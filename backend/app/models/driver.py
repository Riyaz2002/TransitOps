from datetime import date, datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SQLEnum, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import Base


class DriverStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    OFF_DUTY = "Off Duty"
    SUSPENDED = "Suspended"


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    license_category: Mapped[str] = mapped_column(String(50), nullable=False)
    license_expiry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    contact_number: Mapped[str] = mapped_column(String(30), nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, nullable=False, default=100)
    status: Mapped[DriverStatus] = mapped_column(
        SQLEnum(DriverStatus, name="driver_status", native_enum=False),
        nullable=False,
        default=DriverStatus.AVAILABLE,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
