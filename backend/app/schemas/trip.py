from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.trip import TripStatus


class TripBase(BaseModel):
    source: str = Field(min_length=1, max_length=120)
    destination: str = Field(min_length=1, max_length=120)
    vehicle_id: int | None = None
    driver_id: int | None = None
    cargo_weight: float = Field(default=0, ge=0)
    planned_distance: float = Field(default=0, ge=0)
    actual_distance: float | None = Field(default=None, ge=0)
    start_odometer: float = Field(default=0, ge=0)
    end_odometer: float = Field(default=0, ge=0)
    fuel_consumed: float | None = Field(default=None, ge=0)
    status: TripStatus = TripStatus.DRAFT


class TripCreate(TripBase):
    trip_number: str | None = Field(default=None, min_length=1, max_length=50)


class TripUpdate(BaseModel):
    trip_number: str | None = Field(default=None, min_length=1, max_length=50)
    source: str | None = Field(default=None, min_length=1, max_length=120)
    destination: str | None = Field(default=None, min_length=1, max_length=120)
    vehicle_id: int | None = None
    driver_id: int | None = None
    cargo_weight: float | None = Field(default=None, ge=0)
    planned_distance: float | None = Field(default=None, ge=0)
    actual_distance: float | None = Field(default=None, ge=0)
    start_odometer: float | None = Field(default=None, ge=0)
    end_odometer: float | None = Field(default=None, ge=0)
    fuel_consumed: float | None = Field(default=None, ge=0)
    status: TripStatus | None = None


class TripRead(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_number: str | None
    created_at: datetime
    updated_at: datetime
