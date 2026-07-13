"""Pydantic request/response schemas, one module per resource.

Re-exported here so existing ``from app.schemas import X`` imports keep working.
"""

from app.schemas.driver import DriverBase, DriverCreate, DriverRead, DriverUpdate
from app.schemas.maintenance import (
    MaintenanceBase,
    MaintenanceCreate,
    MaintenanceRead,
    MaintenanceUpdate,
)
from app.schemas.trip import TripBase, TripCreate, TripRead, TripUpdate
from app.schemas.user import LoginRequest, RoleUpdate, Token, UserCreate, UserRead
from app.schemas.vehicle import VehicleBase, VehicleCreate, VehicleRead, VehicleUpdate
