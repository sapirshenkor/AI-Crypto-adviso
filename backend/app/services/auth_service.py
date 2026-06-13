import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized_email = email.lower()
    return db.scalar(select(User).where(User.email == normalized_email))


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def email_exists(db: Session, email: str) -> bool:
    return get_user_by_email(db, email) is not None


def create_user(db: Session, name: str, email: str, password: str) -> User:
    user = User(
        name=name,
        email=email.lower(),
        password_hash=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Return the user only when both email and password match."""
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user
