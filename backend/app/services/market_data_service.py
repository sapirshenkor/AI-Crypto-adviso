from app.core.config import settings
from app.data.dashboard_fallbacks import ASSET_SYMBOLS, static_prices_for_assets
from app.schemas.dashboard import PriceItem
from app.schemas.dashboard_context import DashboardContext
from app.services.http_client import get_json

# Internal CoinGecko IDs differ from onboarding asset IDs for some assets.
COINGECKO_ID_BY_ASSET = {
    "bitcoin": "bitcoin",
    "ethereum": "ethereum",
    "solana": "solana",
    "xrp": "ripple",
}

ASSET_BY_COINGECKO_ID = {value: key for key, value in COINGECKO_ID_BY_ASSET.items()}


def _normalize_prices(data: dict, assets: list[str]) -> list[PriceItem]:
    items: list[PriceItem] = []
    for asset in assets:
        coingecko_id = COINGECKO_ID_BY_ASSET.get(asset)
        if not coingecko_id:
            continue

        asset_data = data.get(coingecko_id)
        if not isinstance(asset_data, dict):
            continue

        price_usd = asset_data.get("usd")
        change_24h = asset_data.get("usd_24h_change")
        if price_usd is None or change_24h is None:
            continue

        items.append(
            PriceItem(
                id=f"price_{asset}",
                asset=asset,
                symbol=ASSET_SYMBOLS[asset],
                price_usd=float(price_usd),
                change_24h_percent=float(change_24h),
            )
        )
    return items


def get_prices(context: DashboardContext) -> list[PriceItem]:
    assets = context.assets
    if not settings.coingecko_demo_api_key:
        return static_prices_for_assets(assets)

    coingecko_ids = [
        COINGECKO_ID_BY_ASSET[asset]
        for asset in assets
        if asset in COINGECKO_ID_BY_ASSET
    ]
    if not coingecko_ids:
        return static_prices_for_assets(assets)

    data = get_json(
        f"{settings.coingecko_api_base_url.rstrip('/')}/simple/price",
        headers={"x-cg-demo-api-key": settings.coingecko_demo_api_key},
        params={
            "ids": ",".join(coingecko_ids),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        },
    )
    if not data:
        return static_prices_for_assets(assets)

    prices = _normalize_prices(data, assets)
    return prices or static_prices_for_assets(assets)
