from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from datetime import datetime
from sqlalchemy import DateTime, func

class VehicleStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    IN_SHOP = "In Shop"
    RETIRED = "Retired"
    
class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    registration_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    model_name: Mapped[str] = mapped_column(String(120))
    vehicle_type: Mapped[str] = mapped_column(String(50))
    max_load_capacity: Mapped[float] = mapped_column(Float)
    odometer: Mapped[float] = mapped_column(Float, default=0)
    acquisition_cost: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[VehicleStatus] = mapped_column(
    SQLEnum(VehicleStatus),
    default=VehicleStatus.AVAILABLE,
    index=True,
)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )