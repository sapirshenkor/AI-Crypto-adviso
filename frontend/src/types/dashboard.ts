export interface NewsItem {
  id: string
  title: string
  summary: string
  source: string
  url: string | null
  tags: string[]
}

export interface PriceItem {
  id: string
  asset: string
  symbol: string
  price_usd: number
  change_24h_percent: number
}

export interface AIInsightItem {
  id: string
  title: string
  content: string
  tags: string[]
}

export interface MemeItem {
  id: string
  title: string
  image_url: string
  tags: string[]
}

export interface DashboardResponse {
  news: NewsItem[]
  prices: PriceItem[]
  ai_insight: AIInsightItem
  meme: MemeItem
}
