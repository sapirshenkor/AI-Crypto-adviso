from sqlalchemy.orm import Session

from app.data.dashboard_fallbacks import DEFAULT_ASSETS
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.schemas.dashboard_context import DashboardContext
from app.schemas.onboarding import OnboardingPreferencesResponse
from app.services import (
    ai_insight_service,
    market_data_service,
    meme_service,
    news_service,
    onboarding_service,
)


def _build_context(
    preferences: OnboardingPreferencesResponse,
) -> DashboardContext:
    use_defaults = (
        not preferences.onboarding_completed or not preferences.assets
    )
    assets = DEFAULT_ASSETS if use_defaults else preferences.assets

    return DashboardContext(
        assets=assets,
        investor_type=preferences.investor_type,
        content_types=preferences.content_types,
        onboarding_completed=preferences.onboarding_completed,
        use_defaults=use_defaults,
    )


def build_dashboard(db: Session, user: User) -> DashboardResponse:
    """Orchestrate provider services into the stable dashboard contract."""
    preferences = onboarding_service.get_user_preferences(db, user)
    context = _build_context(preferences)

    prices = market_data_service.get_prices(context)
    news = news_service.get_news(context)
    ai_insight = ai_insight_service.get_insight(context, news, prices)
    meme = meme_service.get_meme(context)

    return DashboardResponse(
        news=news,
        prices=prices,
        ai_insight=ai_insight,
        meme=meme,
    )
