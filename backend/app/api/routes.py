"""Top-level API router that mounts every feature router under /api/v1.

Endpoint definitions live in app/routers/*. This module only wires them together.
"""

from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.driver import router as driver_router
from app.routers.maintenance import router as maintenance_router
from app.routers.trip import router as trip_router
from app.routers.user import router as user_router
from app.routers.vehicle import router as vehicle_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(vehicle_router)
router.include_router(driver_router)

router.include_router(trip_router)
router.include_router(maintenance_router)
