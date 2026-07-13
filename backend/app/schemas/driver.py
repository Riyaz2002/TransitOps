from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.driver import DriverStatus


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
