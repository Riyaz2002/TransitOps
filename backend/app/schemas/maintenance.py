from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.maintenance import MaintenanceStatus, MaintenanceType


class MaintenanceBase(BaseModel):
    vehicle_id: int
    maintenance_type: MaintenanceType
    description: str | None = Field(default=None, max_length=1000)
    cost: float = Field(default=0, ge=0)
    status: MaintenanceStatus = MaintenanceStatus.OPEN


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    maintenance_type: MaintenanceType | None = None
    description: str | None = Field(default=None, max_length=1000)
    cost: float | None = Field(default=None, ge=0)
    status: MaintenanceStatus | None = None
    end_date: datetime | None = None


class MaintenanceRead(MaintenanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    start_date: datetime
    end_date: datetime | None
    created_at: datetime
    updated_at: datetime
