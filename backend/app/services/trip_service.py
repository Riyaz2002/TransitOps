from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.trip import Trip, TripStatus
from app.schemas.trip import TripCreate, TripUpdate


class TripService:
    def __init__(self, db: Session):
        self.db = db

    def create_trip(self, payload: TripCreate) -> Trip:
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
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(trip, field, value)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def dispatch_trip(self, trip_id: int) -> Trip:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.DRAFT:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trip can only be dispatched from Draft")
        trip.status = TripStatus.DISPATCHED
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def complete_trip(self, trip_id: int) -> Trip:
        trip = self.get_trip(trip_id)
        if trip.status != TripStatus.DISPATCHED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trip can only be completed from Dispatched")
        trip.status = TripStatus.COMPLETED
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def cancel_trip(self, trip_id: int) -> Trip:
        trip = self.get_trip(trip_id)
        if trip.status in {TripStatus.COMPLETED, TripStatus.CANCELLED}:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trip cannot be cancelled in its current state")
        trip.status = TripStatus.CANCELLED
        self.db.commit()
        self.db.refresh(trip)
        return trip
