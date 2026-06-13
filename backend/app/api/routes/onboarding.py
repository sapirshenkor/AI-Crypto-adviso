from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.onboarding import (
    OnboardingOptionsResponse,
    OnboardingPreferencesResponse,
    OnboardingPreferencesUpdate,
)
from app.services import onboarding_service

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.get(
    "/options",
    response_model=OnboardingOptionsResponse,
    summary="Get onboarding questionnaire options",
    description=(
        "Returns the static list of allowed assets, investor types, and content types. "
        "Requires a valid Bearer JWT."
    ),
)
def read_onboarding_options(
    current_user: User = Depends(get_current_user),
) -> OnboardingOptionsResponse:
    return onboarding_service.get_onboarding_options()


@router.get(
    "/preferences",
    response_model=OnboardingPreferencesResponse,
    summary="Get the current user's onboarding preferences",
    description=(
        "Returns saved preferences for the authenticated user. "
        "If onboarding has not been completed yet, returns an empty default state."
    ),
)
def read_onboarding_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OnboardingPreferencesResponse:
    return onboarding_service.get_user_preferences(db, current_user)


@router.put(
    "/preferences",
    response_model=OnboardingPreferencesResponse,
    summary="Save or update onboarding preferences",
    description=(
        "Creates preferences on first save or updates the existing row. "
        "Sets onboarding_completed to true. Assets and content_types must each "
        "contain at least one allowed value; investor_type is required."
    ),
)
def save_onboarding_preferences(
    payload: OnboardingPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OnboardingPreferencesResponse:
    return onboarding_service.upsert_user_preferences(db, current_user, payload)
