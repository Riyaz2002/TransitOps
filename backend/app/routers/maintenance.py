from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.models import User
from app.schemas.maintenance import MaintenanceCreate, MaintenanceRead, MaintenanceUpdate
from app.services.maintenance_service import MaintenanceService

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.post("", response_model=MaintenanceRead, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    payload: MaintenanceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
) -> MaintenanceRead:
    """Create a new maintenance record. Automatically sets vehicle status to 'In Shop'."""
    return MaintenanceService(db).create_maintenance(payload)


@router.get("", response_model=list[MaintenanceRead])
def list_maintenance(
    vehicle_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[MaintenanceRead]:
    """List all maintenance records, optionally filtered by vehicle."""
    return MaintenanceService(db).list_maintenance(vehicle_id=vehicle_id)


@router.get("/{maintenance_id}", response_model=MaintenanceRead)
def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
) -> MaintenanceRead:
    """Get a specific maintenance record by ID."""
    return MaintenanceService(db).get_maintenance(maintenance_id)


@router.patch("/{maintenance_id}", response_model=MaintenanceRead)
def update_maintenance(
    maintenance_id: int,
    payload: MaintenanceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
) -> MaintenanceRead:
    """Update a maintenance record."""
    return MaintenanceService(db).update_maintenance(maintenance_id, payload)


@router.post("/{maintenance_id}/close", response_model=MaintenanceRead)
def close_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
) -> MaintenanceRead:
    """Close a maintenance record and restore vehicle to Available status."""
    return MaintenanceService(db).close_maintenance(maintenance_id)


@router.get("/vehicle/{vehicle_id}/open", response_model=list[MaintenanceRead])
def list_open_maintenance_for_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
) -> list[MaintenanceRead]:
    """Get all open maintenance records for a specific vehicle."""
    return MaintenanceService(db).list_open_maintenance_for_vehicle(vehicle_id)
