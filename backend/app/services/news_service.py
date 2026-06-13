from typing import Any

from app.core.config import settings
from app.data.dashboard_fallbacks import static_news_for_assets
from app.schemas.dashboard import NewsItem
from app.schemas.dashboard_context import DashboardContext
from app.services.http_client import get_json

MAX_NEWS_ITEMS = 5


def _build_query(context: DashboardContext) -> str:
    if context.wants_market_news:
        return " OR ".join(context.assets)
    return "crypto"


def _infer_tags(title: str, description: str, context: DashboardContext) -> list[str]:
    text = f"{title} {description}".lower()
    tags: list[str] = []
    for asset in context.assets:
        if asset in text or asset.replace("xrp", "ripple") in text:
            tags.append(asset)
    if context.wants_market_news:
        tags.append("market_news")
    else:
        tags.append("crypto")
    return list(dict.fromkeys(tags)) or ["crypto"]


def _normalize_articles(
    articles: list[dict[str, Any]],
    context: DashboardContext,
) -> list[NewsItem]:
    items: list[NewsItem] = []
    for index, article in enumerate(articles[:MAX_NEWS_ITEMS]):
        title = article.get("title")
        if not isinstance(title, str) or not title.strip():
            continue

        description = article.get("description")
        summary = description if isinstance(description, str) and description.strip() else title
        article_id = article.get("article_id")
        source_name = article.get("source_name")
        link = article.get("link")

        items.append(
            NewsItem(
                id=str(article_id or f"news_live_{index + 1}"),
                title=title.strip(),
                summary=summary.strip(),
                source=str(source_name or "NewsData"),
                url=link if isinstance(link, str) else None,
                tags=_infer_tags(title, summary, context),
            )
        )
    return items


def _fetch_news(query: str) -> list[dict[str, Any]]:
    if not settings.news_data_api_key:
        return []

    data = get_json(
        f"{settings.news_data_api_base_url.rstrip('/')}/crypto",
        params={
            "apikey": settings.news_data_api_key,
            "q": query,
            "language": "en",
        },
    )
    if not data or data.get("status") != "success":
        return []

    results = data.get("results")
    if not isinstance(results, list):
        return []

    return results


def get_news(context: DashboardContext) -> list[NewsItem]:
    query = _build_query(context)
    raw_articles = _fetch_news(query)
    items = _normalize_articles(raw_articles, context) if raw_articles else []

    if items:
        return items

    # Empty API result or provider failure: use static fallback to keep the section populated.
    return static_news_for_assets(
        context.assets,
        general=not context.wants_market_news,
    )
