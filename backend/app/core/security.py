from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# bcrypt is a standard one-way hash; passlib handles salting and verification.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str) -> str:
    """Build a signed JWT; `sub` holds the user id, `exp` enforces expiry."""
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> str | None:
    """Return the user id from a valid token, or None if invalid or expired."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError:
        return None

    subject = payload.get("sub")
    if subject is None:
        return None
    return str(subject)
