from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.models import User, UserRole
from app.db.session import get_db
from app.models.driver import Driver, DriverStatus
from app.schemas.driver import DriverCreate, DriverRead, DriverUpdate

router = APIRouter(tags=["drivers"])


@router.post("/drivers", response_model=DriverRead, status_code=status.HTTP_201_CREATED)
def create_driver(
    payload: DriverCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
) -> Driver:
    license_number = payload.license_number.strip().upper()
    exists = db.scalar(select(Driver.id).where(Driver.license_number == license_number))
    if exists is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="License number already exists")
    driver = Driver(**payload.model_dump(exclude={"license_number"}), license_number=license_number)
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


@router.get("/drivers", response_model=list[DriverRead])
def list_drivers(
    status_filter: DriverStatus | None = None,
    license_valid: bool | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Driver]:
    query = select(Driver).order_by(Driver.created_at.desc())
    if status_filter:
        query = query.where(Driver.status == status_filter)
    if license_valid is True:
        query = query.where(Driver.license_expiry_date >= date.today())
    elif license_valid is False:
        query = query.where(Driver.license_expiry_date < date.today())
    return list(db.scalars(query))


@router.get("/drivers/{driver_id}", response_model=DriverRead)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Driver:
    driver = db.get(Driver, driver_id)
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    return driver


@router.patch("/drivers/{driver_id}", response_model=DriverRead)
def update_driver(
    driver_id: int,
    payload: DriverUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
) -> Driver:
    driver = db.get(Driver, driver_id)
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    changes = payload.model_dump(exclude_unset=True)
    if "license_number" in changes:
        changes["license_number"] = changes["license_number"].strip().upper()
        exists = db.scalar(
            select(Driver.id).where(
                Driver.license_number == changes["license_number"], Driver.id != driver_id
            )
        )
        if exists is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="License number already exists")
    for field, value in changes.items():
        setattr(driver, field, value)
    db.commit()
    db.refresh(driver)
    return driver
