from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.dashboard import (
    AIInsightItem,
    DashboardResponse,
    MemeItem,
    NewsItem,
    PriceItem,
)
from app.schemas.onboarding import OnboardingPreferencesResponse
from app.services import onboarding_service

# Placeholder dashboard content; replaced by external APIs in later phases.
_DEFAULT_ASSETS = ["bitcoin", "ethereum"]

_ASSET_SYMBOLS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "xrp": "XRP",
}

_NEWS_BY_ASSET: dict[str, NewsItem] = {
    "bitcoin": NewsItem(
        id="news_bitcoin_1",
        title="Bitcoin ETF inflows continue to shape market sentiment",
        summary="Institutional interest remains one of the key narratives around Bitcoin.",
        source="Static Demo",
        url=None,
        tags=["bitcoin", "market_news"],
    ),
    "ethereum": NewsItem(
        id="news_ethereum_1",
        title="Ethereum developers discuss the next protocol upgrade",
        summary="Network upgrades and scaling remain central themes for Ethereum investors.",
        source="Static Demo",
        url=None,
        tags=["ethereum", "market_news"],
    ),
    "solana": NewsItem(
        id="news_solana_1",
        title="Solana ecosystem activity draws renewed attention",
        summary="High throughput and active DeFi usage keep Solana in the spotlight.",
        source="Static Demo",
        url=None,
        tags=["solana", "market_news"],
    ),
    "xrp": NewsItem(
        id="news_xrp_1",
        title="XRP market watchers track regulatory and liquidity trends",
        summary="Legal clarity and exchange flows remain key talking points for XRP.",
        source="Static Demo",
        url=None,
        tags=["xrp", "market_news"],
    ),
}

_PRICES_BY_ASSET: dict[str, PriceItem] = {
    "bitcoin": PriceItem(
        id="price_bitcoin",
        asset="bitcoin",
        symbol="BTC",
        price_usd=65000.0,
        change_24h_percent=2.4,
    ),
    "ethereum": PriceItem(
        id="price_ethereum",
        asset="ethereum",
        symbol="ETH",
        price_usd=3500.0,
        change_24h_percent=1.8,
    ),
    "solana": PriceItem(
        id="price_solana",
        asset="solana",
        symbol="SOL",
        price_usd=145.0,
        change_24h_percent=3.1,
    ),
    "xrp": PriceItem(
        id="price_xrp",
        asset="xrp",
        symbol="XRP",
        price_usd=0.62,
        change_24h_percent=-0.5,
    ),
}

_DEFAULT_MEME = MemeItem(
    id="meme_neutral_1",
    title="Crypto markets: where a 2% move feels like a lifetime",
    image_url="https://example.com/static-meme-neutral.png",
    tags=["crypto"],
)

_FUN_MEMES_BY_ASSET: dict[str, MemeItem] = {
    "bitcoin": MemeItem(
        id="meme_bitcoin_1",
        title="When Bitcoin moves 2% and everyone calls it a bull market",
        image_url="https://example.com/static-meme-bitcoin.png",
        tags=["bitcoin", "fun"],
    ),
    "ethereum": MemeItem(
        id="meme_ethereum_1",
        title="Me explaining gas fees to a friend who just bought their first NFT",
        image_url="https://example.com/static-meme-ethereum.png",
        tags=["ethereum", "fun"],
    ),
    "solana": MemeItem(
        id="meme_solana_1",
        title="Solana speedrun: 100 transactions before your coffee gets cold",
        image_url="https://example.com/static-meme-solana.png",
        tags=["solana", "fun"],
    ),
    "xrp": MemeItem(
        id="meme_xrp_1",
        title="XRP holders refreshing the chart like it's a group chat",
        image_url="https://example.com/static-meme-xrp.png",
        tags=["xrp", "fun"],
    ),
}


def _should_use_default_dashboard(
    preferences: OnboardingPreferencesResponse,
) -> bool:
    """Use general content when onboarding is incomplete or assets are unset."""
    return (
        not preferences.onboarding_completed
        or not preferences.assets
    )


def _resolve_assets(preferences: OnboardingPreferencesResponse) -> list[str]:
    if _should_use_default_dashboard(preferences):
        return _DEFAULT_ASSETS
    return preferences.assets


def _build_news(
    preferences: OnboardingPreferencesResponse,
    assets: list[str],
) -> list[NewsItem]:
    if _should_use_default_dashboard(preferences):
        return [_NEWS_BY_ASSET[asset] for asset in _DEFAULT_ASSETS]

    if "market_news" not in preferences.content_types:
        return []

    return [_NEWS_BY_ASSET[asset] for asset in assets if asset in _NEWS_BY_ASSET]


def _build_prices(assets: list[str]) -> list[PriceItem]:
    return [_PRICES_BY_ASSET[asset] for asset in assets if asset in _PRICES_BY_ASSET]


def _format_asset_list(assets: list[str]) -> str:
    labels = [asset.replace("_", " ").title() for asset in assets]
    if len(labels) == 1:
        return labels[0]
    return ", ".join(labels[:-1]) + f" and {labels[-1]}"


def _build_ai_insight(
    preferences: OnboardingPreferencesResponse,
    assets: list[str],
) -> AIInsightItem:
    asset_text = _format_asset_list(assets)
    tags = list(dict.fromkeys(assets + preferences.content_types))

    if _should_use_default_dashboard(preferences):
        return AIInsightItem(
            id="insight_default_1",
            title="AI Insight of the Day",
            content=(
                "Welcome to your crypto dashboard. Explore general market themes "
                "around Bitcoin and Ethereum while you complete onboarding."
            ),
            tags=["bitcoin", "ethereum", "market_news"],
        )

    content_parts = [f"Based on your interest in {asset_text}"]

    if "market_news" in preferences.content_types:
        content_parts.append("market news")
    if "charts" in preferences.content_types:
        content_parts.append("price charts")
    if "social" in preferences.content_types:
        content_parts.append("social sentiment")
    if "fun" in preferences.content_types:
        content_parts.append("lighter crypto content")

    interests = ", ".join(content_parts[1:]) if len(content_parts) > 1 else ""
    if interests:
        content = (
            f"{content_parts[0]} and {interests}, today's main theme is "
            f"watching how your selected assets fit the current market mood."
        )
    else:
        content = (
            f"{content_parts[0]}, today's main theme is tracking how your "
            "selected assets are moving in the broader crypto market."
        )

    if preferences.investor_type == "hodler":
        content += " As a HODLer, focus on long-term narratives over short-term noise."
    elif preferences.investor_type == "day_trader":
        content += " As a day trader, watch intraday volatility and liquidity closely."
    elif preferences.investor_type == "nft_collector":
        content += " As an NFT collector, ecosystem activity may matter as much as price."

    return AIInsightItem(
        id="insight_static_1",
        title="AI Insight of the Day",
        content=content,
        tags=tags,
    )


def _build_meme(
    preferences: OnboardingPreferencesResponse,
    assets: list[str],
) -> MemeItem:
    wants_fun = (
        _should_use_default_dashboard(preferences)
        or "fun" in preferences.content_types
    )

    if not wants_fun:
        return _DEFAULT_MEME

    for asset in assets:
        if asset in _FUN_MEMES_BY_ASSET:
            return _FUN_MEMES_BY_ASSET[asset]

    return MemeItem(
        id="meme_fun_general_1",
        title="When the portfolio is green and you pretend you planned it all along",
        image_url="https://example.com/static-meme-fun.png",
        tags=["fun", "crypto"],
    )


def build_dashboard(db: Session, user: User) -> DashboardResponse:
    """Read user preferences and assemble a rule-based static dashboard."""
    preferences = onboarding_service.get_user_preferences(db, user)
    assets = _resolve_assets(preferences)

    return DashboardResponse(
        news=_build_news(preferences, assets),
        prices=_build_prices(assets),
        ai_insight=_build_ai_insight(preferences, assets),
        meme=_build_meme(preferences, assets),
    )
