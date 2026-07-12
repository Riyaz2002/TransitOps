from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trip import Trip, TripStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.models.driver import Driver, DriverStatus
from app.schemas.trip import TripCreate, TripUpdate


class TripService:
    def __init__(self, db: Session):
        self.db = db

    def create_trip(self, payload: TripCreate) -> Trip:
        # Validate vehicle if provided
        if payload.vehicle_id is not None:
            vehicle = self.db.get(Vehicle, payload.vehicle_id)
            if vehicle is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
            if vehicle.status in {VehicleStatus.IN_SHOP, VehicleStatus.RETIRED}:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Vehicle status is {vehicle.status.value} and cannot be used for trips"
                )
            if vehicle.max_load_capacity < payload.cargo_weight:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Cargo weight {payload.cargo_weight} exceeds vehicle capacity {vehicle.max_load_capacity}"
                )

        # Validate driver if provided
        if payload.driver_id is not None:
            driver = self.db.get(Driver, payload.driver_id)
            if driver is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
            if driver.status in {DriverStatus.SUSPENDED}:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Driver status is {driver.status.value} and cannot be assigned to trips"
                )

        trip = Trip(**payload.model_dump(exclude_none=True))
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def get_trip(self, trip_id: int) -> Trip:
        trip = self.db.get(Trip, trip_id)
        if trip is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        return trip

    def list_trips(self) -> list[Trip]:
        return list(self.db.scalars(select(Trip).order_by(Trip.created_at.desc())).all())

    def update_trip(self, trip_id: int, payload: TripUpdate) -> Trip:
        trip = self.get_trip(trip_id)
        
        # Validate vehicle if being updated
        if payload.vehicle_id is not None and payload.vehicle_id != trip.vehicle_id:
            vehicle = self.db.get(Vehicle, payload.vehicle_id)
            if vehicle is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
            if vehicle.status in {VehicleStatus.IN_SHOP, VehicleStatus.RETIRED}:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Vehicle status is {vehicle.status.value} and cannot be used for trips"
                )
        
        # Validate driver if being updated
        if payload.driver_id is not None and payload.driver_id != trip.driver_id:
            driver = self.db.get(Driver, payload.driver_id)
            if driver is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
            if driver.status in {DriverStatus.SUSPENDED}:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Driver status is {driver.status.value} and cannot be assigned to trips"
                )
        
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(trip, field, value)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def dispatch_trip(self, trip_id: int) -> Trip:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.DRAFT:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trip can only be dispatched from Draft")
        
        # Final validation before dispatch
        if trip.vehicle_id is not None:
            vehicle = self.db.get(Vehicle, trip.vehicle_id)
            if vehicle is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
            if vehicle.status != VehicleStatus.AVAILABLE:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Vehicle is {vehicle.status.value} and cannot be dispatched"
                )
            # Update vehicle status to On Trip
            vehicle.status = VehicleStatus.ON_TRIP
            self.db.add(vehicle)
        
        if trip.driver_id is not None:
            driver = self.db.get(Driver, trip.driver_id)
            if driver is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
            if driver.status != DriverStatus.AVAILABLE:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Driver is {driver.status.value} and cannot be dispatched"
                )
            # Update driver status to On Trip
            driver.status = DriverStatus.ON_TRIP
            self.db.add(driver)
        
        trip.status = TripStatus.DISPATCHED
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def complete_trip(self, trip_id: int) -> Trip:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.DISPATCHED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trip can only be completed from Dispatched")
        
        # Restore vehicle and driver to Available
        if trip.vehicle_id is not None:
            vehicle = self.db.get(Vehicle, trip.vehicle_id)
            if vehicle is not None:
                vehicle.status = VehicleStatus.AVAILABLE
                self.db.add(vehicle)
        
        if trip.driver_id is not None:
            driver = self.db.get(Driver, trip.driver_id)
            if driver is not None:
                driver.status = DriverStatus.AVAILABLE
                self.db.add(driver)
        
        trip.status = TripStatus.COMPLETED
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def cancel_trip(self, trip_id: int) -> Trip:
        trip = self.get_trip(trip_id)
        if trip.status in {TripStatus.COMPLETED, TripStatus.CANCELLED}:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trip cannot be cancelled in its current state")
        
        # Restore vehicle and driver to Available if trip was dispatched
        if trip.status == TripStatus.DISPATCHED:
            if trip.vehicle_id is not None:
                vehicle = self.db.get(Vehicle, trip.vehicle_id)
                if vehicle is not None:
                    vehicle.status = VehicleStatus.AVAILABLE
                    self.db.add(vehicle)
            
            if trip.driver_id is not None:
                driver = self.db.get(Driver, trip.driver_id)
                if driver is not None:
                    driver.status = DriverStatus.AVAILABLE
                    self.db.add(driver)
        
        trip.status = TripStatus.CANCELLED
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip
