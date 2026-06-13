from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create an account with name, email, and password. Returns the user profile without the password hash.",
)
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> User:
    if auth_service.email_exists(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return auth_service.create_user(
        db, name=payload.name, email=payload.email, password=payload.password
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and receive a JWT",
    description="Authenticate with email and password. Returns a bearer access token for protected routes.",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    if user is None:
        # Same message for unknown email or wrong password.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(str(user.id))
    return TokenResponse(access_token=access_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get the current authenticated user",
    description="Requires a valid Bearer JWT. Use the Authorize button in Swagger to paste the token from login.",
)
def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user
