from datetime import datetime, timezone

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.core.config import get_settings
from app.core.security import (
    ALGORITHM,
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token_id,
    verify_password,
)
from app.db.models import RefreshToken, User, UserRole
from app.db.session import get_db
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas import (
    LoginRequest,
    RoleUpdate,
    Token,
    UserCreate,
    UserRead,
    VehicleCreate,
    VehicleRead,
    VehicleUpdate,
)

router = APIRouter(prefix="/api/v1")
REFRESH_TOKEN_COOKIE = "refresh_token"


def set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=settings.refresh_token_cookie_secure,
        samesite="lax",
        path="/api/v1/auth",
    )


@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    email = str(payload.email).lower()
    if db.scalar(select(User.id).where(User.email == email)) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    user = User(email=email, full_name=payload.full_name.strip(), hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=Token)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> Token:
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if user is None or not user.is_active or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    refresh_token, token_id, expires_at = create_refresh_token(str(user.id))
    db.add(RefreshToken(user_id=user.id, token_id_hash=hash_token_id(token_id), expires_at=expires_at))
    db.commit()
    set_refresh_token_cookie(response, refresh_token)
    return Token(access_token=create_access_token(str(user.id)))


@router.post("/auth/refresh", response_model=Token)
def refresh_access_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_TOKEN_COOKIE),
    db: Session = Depends(get_db),
) -> Token:
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    if refresh_token is None:
        raise unauthorized
    try:
        payload = jwt.decode(refresh_token, get_settings().secret_key, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        token_id = payload.get("jti")
        if not subject or not token_id or payload.get("type") != REFRESH_TOKEN_TYPE:
            raise unauthorized
        user_id = int(subject)
    except (jwt.PyJWTError, TypeError, ValueError):
        raise unauthorized

    stored_token = db.scalar(
        select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.token_id_hash == hash_token_id(token_id),
            RefreshToken.revoked_at.is_(None),
        )
    )
    user = db.get(User, user_id)
    if stored_token is None or stored_token.expires_at <= datetime.now(timezone.utc) or user is None or not user.is_active:
        raise unauthorized

    stored_token.revoked_at = datetime.now(timezone.utc)
    new_refresh_token, new_token_id, expires_at = create_refresh_token(str(user.id))
    db.add(RefreshToken(user_id=user.id, token_id_hash=hash_token_id(new_token_id), expires_at=expires_at))
    db.commit()
    set_refresh_token_cookie(response, new_refresh_token)
    return Token(access_token=create_access_token(str(user.id)))


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=REFRESH_TOKEN_COOKIE),
    db: Session = Depends(get_db),
) -> Response:
    if refresh_token is not None:
        try:
            payload = jwt.decode(refresh_token, get_settings().secret_key, algorithms=[ALGORITHM])
            token_id = payload.get("jti")
            if payload.get("type") == REFRESH_TOKEN_TYPE and token_id:
                stored_token = db.scalar(
                    select(RefreshToken).where(RefreshToken.token_id_hash == hash_token_id(token_id))
                )
                if stored_token is not None and stored_token.revoked_at is None:
                    stored_token.revoked_at = datetime.now(timezone.utc)
                    db.commit()
        except jwt.PyJWTError:
            pass
    response.delete_cookie(key=REFRESH_TOKEN_COOKIE, path="/api/v1/auth")
    return response


@router.get("/auth/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.patch("/users/{user_id}/role", response_model=UserRead)
def update_user_role(
    user_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = payload.role
    db.commit()
    db.refresh(user)
    return user


@router.get("/dispatches", response_model=list[str])
def list_dispatches(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.DISPATCHER))) -> list[str]:
    """Example route: replace with the real dispatch resource."""
    return []


@router.post("/vehicles", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
) -> Vehicle:
    registration_number = payload.registration_number.strip().upper()
    exists = db.scalar(select(Vehicle.id).where(Vehicle.registration_number == registration_number))
    if exists is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration number already exists")

    vehicle = Vehicle(**payload.model_dump(exclude={"registration_number"}), registration_number=registration_number)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.get("/vehicles", response_model=list[VehicleRead])
def list_vehicles(
    vehicle_type: str | None = None,
    status_filter: VehicleStatus | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Vehicle]:
    query = select(Vehicle).order_by(Vehicle.created_at.desc())
    if vehicle_type:
        query = query.where(Vehicle.vehicle_type == vehicle_type)
    if status_filter:
        query = query.where(Vehicle.status == status_filter)
    return list(db.scalars(query))


@router.get("/vehicles/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle


@router.patch("/vehicles/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

    changes = payload.model_dump(exclude_unset=True)
    if "registration_number" in changes:
        changes["registration_number"] = changes["registration_number"].strip().upper()
        exists = db.scalar(
            select(Vehicle.id).where(
                Vehicle.registration_number == changes["registration_number"], Vehicle.id != vehicle_id
            )
        )
        if exists is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration number already exists")
    for field, value in changes.items():
        setattr(vehicle, field, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle
