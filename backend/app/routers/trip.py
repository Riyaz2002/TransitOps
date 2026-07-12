from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.models import User
from app.schemas.trip import TripCreate, TripRead, TripUpdate
from app.services.trip_service import TripService

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("", response_model=TripRead, status_code=status.HTTP_201_CREATED)
def create_trip(payload: TripCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> TripRead:
    return TripService(db).create_trip(payload)


@router.get("", response_model=list[TripRead])
def list_trips(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[TripRead]:
    return TripService(db).list_trips()


@router.get("/{trip_id}", response_model=TripRead)
def get_trip(trip_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> TripRead:
    return TripService(db).get_trip(trip_id)


@router.patch("/{trip_id}", response_model=TripRead)
def update_trip(trip_id: int, payload: TripUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> TripRead:
    return TripService(db).update_trip(trip_id, payload)


@router.post("/{trip_id}/dispatch", response_model=TripRead)
def dispatch_trip(trip_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> TripRead:
    return TripService(db).dispatch_trip(trip_id)


@router.post("/{trip_id}/complete", response_model=TripRead)
def complete_trip(trip_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> TripRead:
    return TripService(db).complete_trip(trip_id)


@router.post("/{trip_id}/cancel", response_model=TripRead)
def cancel_trip(trip_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> TripRead:
    return TripService(db).cancel_trip(trip_id)
