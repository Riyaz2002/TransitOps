from __future__ import annotations

from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance, MaintenanceStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate


class MaintenanceService:
    def __init__(self, db: Session):
        self.db = db

    def create_maintenance(self, payload: MaintenanceCreate) -> Maintenance:
        """
        Create a new maintenance record.
        Automatically sets the vehicle status to "In Shop".
        """
        # Verify vehicle exists
        vehicle = self.db.get(Vehicle, payload.vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
            )

        # Create maintenance record
        maintenance = Maintenance(**payload.model_dump(exclude_none=True))
        self.db.add(maintenance)

        # Update vehicle status to "In Shop"
        vehicle.status = VehicleStatus.IN_SHOP
        self.db.add(vehicle)

        self.db.commit()
        self.db.refresh(maintenance)
        return maintenance

    def get_maintenance(self, maintenance_id: int) -> Maintenance:
        """Get a maintenance record by ID."""
        maintenance = self.db.get(Maintenance, maintenance_id)
        if maintenance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance record not found"
            )
        return maintenance

    def list_maintenance(self, vehicle_id: int | None = None) -> list[Maintenance]:
        """List all maintenance records, optionally filtered by vehicle."""
        query = select(Maintenance).order_by(Maintenance.created_at.desc())
        if vehicle_id is not None:
            query = query.where(Maintenance.vehicle_id == vehicle_id)
        return list(self.db.scalars(query).all())

    def update_maintenance(self, maintenance_id: int, payload: MaintenanceUpdate) -> Maintenance:
        """Update a maintenance record."""
        maintenance = self.get_maintenance(maintenance_id)

        # If closing the maintenance, update vehicle status
        if payload.status == MaintenanceStatus.CLOSED and maintenance.status != MaintenanceStatus.CLOSED:
            vehicle = self.db.get(Vehicle, maintenance.vehicle_id)
            if vehicle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
                )

            # Only restore to Available if vehicle is not Retired
            if vehicle.status != VehicleStatus.RETIRED:
                vehicle.status = VehicleStatus.AVAILABLE

            # Set end_date when closing
            if payload.end_date is None:
                payload.end_date = datetime.now(datetime.now().astimezone().tzinfo)

            self.db.add(vehicle)

        # Update maintenance fields
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(maintenance, field, value)

        self.db.commit()
        self.db.refresh(maintenance)
        return maintenance

    def list_open_maintenance_for_vehicle(self, vehicle_id: int) -> list[Maintenance]:
        """Get all open maintenance records for a vehicle."""
        query = select(Maintenance).where(
            Maintenance.vehicle_id == vehicle_id,
            Maintenance.status == MaintenanceStatus.OPEN
        )
        return list(self.db.scalars(query).all())

    def close_maintenance(self, maintenance_id: int) -> Maintenance:
        """Close a maintenance record and restore vehicle status."""
        maintenance = self.get_maintenance(maintenance_id)

        if maintenance.status != MaintenanceStatus.OPEN:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Can only close maintenance records with Open status"
            )

        vehicle = self.db.get(Vehicle, maintenance.vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
            )

        # Update maintenance status and set end_date
        maintenance.status = MaintenanceStatus.CLOSED
        maintenance.end_date = datetime.now(datetime.now().astimezone().tzinfo)

        # Restore vehicle status to Available if not Retired
        if vehicle.status != VehicleStatus.RETIRED:
            vehicle.status = VehicleStatus.AVAILABLE

        self.db.add(maintenance)
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(maintenance)
        return maintenance
