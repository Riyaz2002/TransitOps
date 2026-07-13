from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.models import User, UserRole
from app.db.session import get_db
from app.schemas.user import RoleUpdate, UserRead

router = APIRouter(tags=["users"])


@router.patch("/users/{user_id}/role", response_model=UserRead)
def update_user_role(
    user_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = payload.role
    db.commit()
    db.refresh(user)
    return user


@router.get("/dispatches", response_model=list[str])
def list_dispatches(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.DISPATCHER))) -> list[str]:
    """Example route: replace with the real dispatch resource."""
    return []
