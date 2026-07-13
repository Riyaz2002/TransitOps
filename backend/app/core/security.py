from datetime import datetime, timedelta, timezone
from hashlib import sha256
from uuid import uuid4

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

ALGORITHM = "HS256"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": subject,
        "type": ACCESS_TOKEN_TYPE,
        "exp": expires_at,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def create_refresh_token(
    subject: str, expires_at: datetime | None = None
) -> tuple[str, str, datetime]:
    """Create a refresh JWT that cannot outlive its original session deadline."""
    settings = get_settings()
    if expires_at is None:
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    token_id = str(uuid4())
    payload = {
        "sub": subject,
        "type": REFRESH_TOKEN_TYPE,
        "jti": token_id,
        "exp": expires_at,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM), token_id, expires_at


def hash_token_id(token_id: str) -> str:
    """Avoid storing a usable refresh-token identifier in the database."""
    return sha256(token_id.encode("utf-8")).hexdigest()
