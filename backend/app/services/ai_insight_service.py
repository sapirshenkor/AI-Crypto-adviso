from app.core.config import settings
from app.data.dashboard_fallbacks import static_insight
from app.schemas.dashboard import AIInsightItem, NewsItem, PriceItem
from app.schemas.dashboard_context import DashboardContext
from app.services.http_client import post_json

SYSTEM_PROMPT = """You are an AI crypto dashboard assistant.

Generate exactly one concise personalized insight.

Rules:
- Maximum 40 words.
- No markdown.
- No bullet points.
- No title.
- No greeting.
- No financial advice.
- No buy/sell/hold recommendations.
- Mention at least one selected asset if available.
- Use the user's investor type and interests when relevant.
- Focus on market awareness and trends.

Return only the insight text."""

MAX_HEADLINES = 5


def _format_assets(assets: list[str]) -> str:
    if not assets:
        return "none selected"
    return ", ".join(assets)


def _format_headlines(news: list[NewsItem]) -> str:
    if not news:
        return "No recent headlines available."
    lines = [f"- {item.title}" for item in news[:MAX_HEADLINES]]
    return "\n".join(lines)


def _format_price_changes(prices: list[PriceItem]) -> str:
    if not prices:
        return "No recent price changes available."
    lines = []
    for price in prices:
        sign = "+" if price.change_24h_percent >= 0 else ""
        lines.append(f"{price.symbol} {sign}{price.change_24h_percent:.1f}%")
    return "\n".join(lines)


def _build_user_prompt(
    context: DashboardContext,
    news: list[NewsItem],
    prices: list[PriceItem],
) -> str:
    investor_type = context.investor_type or "unspecified"
    interests = ", ".join(context.content_types) if context.content_types else "general crypto"

    return (
        f"User assets:\n{_format_assets(context.assets)}\n\n"
        f"Investor type:\n{investor_type}\n\n"
        f"Content interests:\n{interests}\n\n"
        f"Recent headlines:\n{_format_headlines(news)}\n\n"
        f"Recent price changes:\n{_format_price_changes(prices)}\n\n"
        "Generate one personalized dashboard insight."
    )


def _extract_content(data: dict) -> str | None:
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        return None

    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict):
        return None

    content = message.get("content")
    if not isinstance(content, str):
        return None

    cleaned = content.strip().strip('"').strip()
    return cleaned or None


def _request_insight(model: str, user_prompt: str) -> str | None:
    if not settings.openrouter_api_key:
        return None

    data = post_json(
        f"{settings.openrouter_api_base_url.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        },
        json_body={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 120,
            "temperature": 0.7,
        },
    )
    if not data:
        return None
    return _extract_content(data)


def get_insight(
    context: DashboardContext,
    news: list[NewsItem],
    prices: list[PriceItem],
) -> AIInsightItem:
    user_prompt = _build_user_prompt(context, news, prices)
    tags = list(dict.fromkeys(context.assets + context.content_types))

    for model in (settings.openrouter_model, settings.openrouter_fallback_model):
        content = _request_insight(model, user_prompt)
        if content:
            return AIInsightItem(
                id="insight_live_1",
                title="AI Insight of the Day",
                content=content,
                tags=tags,
            )

    return static_insight(
        assets=context.assets,
        investor_type=context.investor_type,
        content_types=context.content_types,
        use_defaults=context.use_defaults,
    )
