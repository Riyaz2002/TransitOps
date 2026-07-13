from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.models import User, UserRole
from app.db.session import get_db
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate

router = APIRouter(tags=["vehicles"])


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
