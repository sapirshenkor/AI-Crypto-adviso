from pydantic import BaseModel


class NewsItem(BaseModel):
    id: str
    title: str
    summary: str
    source: str
    url: str | None
    tags: list[str]


class PriceItem(BaseModel):
    id: str
    asset: str
    symbol: str
    price_usd: float
    change_24h_percent: float


class AIInsightItem(BaseModel):
    id: str
    title: str
    content: str
    tags: list[str]


class MemeItem(BaseModel):
    id: str
    title: str
    image_url: str
    tags: list[str]


class DashboardResponse(BaseModel):
    news: list[NewsItem]
    prices: list[PriceItem]
    ai_insight: AIInsightItem
    meme: MemeItem
