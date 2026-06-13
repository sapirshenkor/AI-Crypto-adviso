from app.schemas.dashboard import AIInsightItem, MemeItem, NewsItem, PriceItem

DEFAULT_ASSETS = ["bitcoin", "ethereum"]

ASSET_SYMBOLS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "xrp": "XRP",
}

NEWS_BY_ASSET: dict[str, NewsItem] = {
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

GENERAL_NEWS = NewsItem(
    id="news_general_1",
    title="Crypto markets watch macro trends and liquidity flows",
    summary="A broad look at how digital assets are moving amid global market conditions.",
    source="Static Demo",
    url=None,
    tags=["crypto", "market_news"],
)

PRICES_BY_ASSET: dict[str, PriceItem] = {
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

DEFAULT_MEME = MemeItem(
    id="meme_neutral_1",
    title="Crypto markets: where a 2% move feels like a lifetime",
    image_url="https://example.com/static-meme-neutral.png",
    tags=["crypto"],
)


def static_news_for_assets(assets: list[str], general: bool = False) -> list[NewsItem]:
    if general:
        return [GENERAL_NEWS, *[NEWS_BY_ASSET[asset] for asset in DEFAULT_ASSETS]]
    items = [NEWS_BY_ASSET[asset] for asset in assets if asset in NEWS_BY_ASSET]
    return items or [GENERAL_NEWS]


def static_prices_for_assets(assets: list[str]) -> list[PriceItem]:
    return [PRICES_BY_ASSET[asset] for asset in assets if asset in PRICES_BY_ASSET]


def static_insight(
    assets: list[str],
    investor_type: str | None,
    content_types: list[str],
    use_defaults: bool,
) -> AIInsightItem:
    asset_labels = [asset.replace("_", " ").title() for asset in assets]
    if len(asset_labels) == 1:
        asset_text = asset_labels[0]
    elif asset_labels:
        asset_text = ", ".join(asset_labels[:-1]) + f" and {asset_labels[-1]}"
    else:
        asset_text = "crypto"

    tags = list(dict.fromkeys(assets + content_types))

    if use_defaults:
        return AIInsightItem(
            id="insight_static_1",
            title="AI Insight of the Day",
            content=(
                "Welcome to your crypto dashboard. Explore general market themes "
                "around Bitcoin and Ethereum while you complete onboarding."
            ),
            tags=["bitcoin", "ethereum", "market_news"],
        )

    content = (
        f"Based on your interest in {asset_text}, today's main theme is tracking "
        "how your selected assets fit the current market mood."
    )

    if investor_type == "hodler":
        content += " As a HODLer, focus on long-term narratives over short-term noise."
    elif investor_type == "day_trader":
        content += " As a day trader, watch intraday volatility and liquidity closely."
    elif investor_type == "nft_collector":
        content += " As an NFT collector, ecosystem activity may matter as much as price."

    return AIInsightItem(
        id="insight_static_1",
        title="AI Insight of the Day",
        content=content,
        tags=tags,
    )
