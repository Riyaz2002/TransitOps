from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import Base


class TripStatus(str, Enum):
    DRAFT = "Draft"
    DISPATCHED = "Dispatched"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_number: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, nullable=True)
    source: Mapped[str] = mapped_column(String(120), nullable=False)
    destination: Mapped[str] = mapped_column(String(120), nullable=False)
    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehicles.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    driver_id: Mapped[int | None] = mapped_column(
        ForeignKey("drivers.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    cargo_weight: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    planned_distance: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    actual_distance: Mapped[float | None] = mapped_column(Float, nullable=True)
    start_odometer: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    end_odometer: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    fuel_consumed: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[TripStatus] = mapped_column(
        SQLEnum(TripStatus, name="trip_status", native_enum=False),
        nullable=False,
        default=TripStatus.DRAFT,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    vehicle: Mapped["Vehicle | None"] = relationship("Vehicle", foreign_keys=[vehicle_id])
    driver: Mapped["Driver | None"] = relationship("Driver", foreign_keys=[driver_id])
