from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, func, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base


class MaintenanceStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"


class MaintenanceType(str, Enum):
    OIL_CHANGE = "Oil Change"
    TIRE_REPLACEMENT = "Tire Replacement"
    BRAKE_SERVICE = "Brake Service"
    ENGINE_REPAIR = "Engine Repair"
    TRANSMISSION_REPAIR = "Transmission Repair"
    ELECTRICAL_REPAIR = "Electrical Repair"
    INSPECTION = "Inspection"
    OTHER = "Other"


class Maintenance(Base):
    __tablename__ = "maintenance_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    maintenance_type: Mapped[MaintenanceType] = mapped_column(
        SQLEnum(MaintenanceType, name="maintenance_type", native_enum=False),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    cost: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    status: Mapped[MaintenanceStatus] = mapped_column(
        SQLEnum(MaintenanceStatus, name="maintenance_status", native_enum=False),
        nullable=False,
        default=MaintenanceStatus.OPEN,
        index=True,
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    vehicle: Mapped["Vehicle"] = relationship("Vehicle", foreign_keys=[vehicle_id])
