from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.vehicle import VehicleStatus


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
