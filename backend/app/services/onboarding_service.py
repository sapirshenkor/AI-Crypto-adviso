from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.schemas.onboarding import (
    OnboardingOptionsResponse,
    OnboardingPreferencesResponse,
    OnboardingPreferencesUpdate,
    OptionItem,
)

# Static questionnaire options; IDs align with CoinGecko, news search, and tags later.
_ASSET_OPTIONS = [
    OptionItem(id="bitcoin", label="Bitcoin"),
    OptionItem(id="ethereum", label="Ethereum"),
    OptionItem(id="solana", label="Solana"),
    OptionItem(id="xrp", label="XRP"),
]
_INVESTOR_TYPE_OPTIONS = [
    OptionItem(id="hodler", label="HODLer"),
    OptionItem(id="day_trader", label="Day Trader"),
    OptionItem(id="nft_collector", label="NFT Collector"),
]
_CONTENT_TYPE_OPTIONS = [
    OptionItem(id="market_news", label="Market News"),
    OptionItem(id="charts", label="Charts"),
    OptionItem(id="social", label="Social"),
    OptionItem(id="fun", label="Fun"),
]


def get_onboarding_options() -> OnboardingOptionsResponse:
    return OnboardingOptionsResponse(
        assets=_ASSET_OPTIONS,
        investor_types=_INVESTOR_TYPE_OPTIONS,
        content_types=_CONTENT_TYPE_OPTIONS,
    )


def _default_preferences_response() -> OnboardingPreferencesResponse:
    return OnboardingPreferencesResponse(
        assets=[],
        investor_type=None,
        content_types=[],
        onboarding_completed=False,
    )


def _to_preferences_response(
    preferences: UserPreferences,
) -> OnboardingPreferencesResponse:
    return OnboardingPreferencesResponse(
        assets=preferences.assets,
        investor_type=preferences.investor_type,
        content_types=preferences.content_types,
        onboarding_completed=preferences.onboarding_completed,
    )


def get_user_preferences(db: Session, user: User) -> OnboardingPreferencesResponse:
    preferences = db.scalar(
        select(UserPreferences).where(UserPreferences.user_id == user.id)
    )
    if preferences is None:
        return _default_preferences_response()
    return _to_preferences_response(preferences)


def upsert_user_preferences(
    db: Session,
    user: User,
    payload: OnboardingPreferencesUpdate,
) -> OnboardingPreferencesResponse:
    """Create a preferences row for the user, or update the existing one."""
    preferences = db.scalar(
        select(UserPreferences).where(UserPreferences.user_id == user.id)
    )

    if preferences is None:
        preferences = UserPreferences(
            user_id=user.id,
            assets=payload.assets,
            investor_type=payload.investor_type,
            content_types=payload.content_types,
            onboarding_completed=True,
        )
        db.add(preferences)
    else:
        preferences.assets = payload.assets
        preferences.investor_type = payload.investor_type
        preferences.content_types = payload.content_types
        preferences.onboarding_completed = True

    db.commit()
    db.refresh(preferences)
    return _to_preferences_response(preferences)
