import { Card } from '../ui/Card'
import { EmptyState } from '../ui/EmptyState'
import type { NewsItem } from '../../types/dashboard'

interface NewsCardProps {
  items: NewsItem[]
}

export function NewsCard({ items }: NewsCardProps) {
  return (
    <Card
      title="Market News"
      subtitle="Latest headlines based on your interests"
    >
      {items.length === 0 ? (
        <EmptyState message="No market news selected yet." />
      ) : (
        <ul className="news-list">
          {items.map((item) => (
            <li key={item.id} className="news-list__item">
              <h3 className="news-list__title">{item.title}</h3>
              <p className="news-list__summary">{item.summary}</p>
              <div className="news-list__meta">
                <span>{item.source}</span>
                <span className="tag-list">
                  {item.tags.map((tag) => (
                    <span key={tag} className="tag">
                      {tag}
                    </span>
                  ))}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}
