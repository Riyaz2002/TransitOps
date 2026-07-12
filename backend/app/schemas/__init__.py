from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.db.models import UserRole
from app.models.driver import DriverStatus
from app.models.trip import TripStatus
from app.models.vehicle import VehicleStatus


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RoleUpdate(BaseModel):
    role: UserRole


class VehicleBase(BaseModel):
    registration_number: str = Field(min_length=1, max_length=50)
    model_name: str = Field(min_length=1, max_length=120)
    vehicle_type: str = Field(min_length=1, max_length=50)
    max_load_capacity: float = Field(gt=0)
    odometer: float = Field(default=0, ge=0)
    acquisition_cost: float = Field(default=0, ge=0)
    status: VehicleStatus = VehicleStatus.AVAILABLE


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    registration_number: str | None = Field(default=None, min_length=1, max_length=50)
    model_name: str | None = Field(default=None, min_length=1, max_length=120)
    vehicle_type: str | None = Field(default=None, min_length=1, max_length=50)
    max_load_capacity: float | None = Field(default=None, gt=0)
    odometer: float | None = Field(default=None, ge=0)
    acquisition_cost: float | None = Field(default=None, ge=0)
    status: VehicleStatus | None = None


class VehicleRead(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class DriverBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    license_number: str = Field(min_length=1, max_length=50)
    license_category: str = Field(min_length=1, max_length=50)
    license_expiry_date: date
    contact_number: str = Field(min_length=5, max_length=30)
    safety_score: float = Field(default=100, ge=0, le=100)
    status: DriverStatus = DriverStatus.AVAILABLE


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    license_number: str | None = Field(default=None, min_length=1, max_length=50)
    license_category: str | None = Field(default=None, min_length=1, max_length=50)
    license_expiry_date: date | None = None
    contact_number: str | None = Field(default=None, min_length=5, max_length=30)
    safety_score: float | None = Field(default=None, ge=0, le=100)
    status: DriverStatus | None = None


class DriverRead(DriverBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


from .trip import TripCreate, TripRead, TripUpdate

__all__ = [
    "UserCreate",
    "LoginRequest",
    "UserRead",
    "Token",
    "RoleUpdate",
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleRead",
    "DriverBase",
    "DriverCreate",
    "DriverUpdate",
    "DriverRead",
    "TripCreate",
    "TripUpdate",
    "TripRead",
]
