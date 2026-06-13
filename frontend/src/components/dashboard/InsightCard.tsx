import { Card } from '../ui/Card'
import type { AIInsightItem } from '../../types/dashboard'

interface InsightCardProps {
  insight: AIInsightItem
}

export function InsightCard({ insight }: InsightCardProps) {
  return (
    <Card
      title={insight.title}
      subtitle="Personalized static insight for your profile"
      className="insight-card"
    >
      <p className="insight-card__content">{insight.content}</p>
      <div className="tag-list">
        {insight.tags.map((tag) => (
          <span key={tag} className="tag tag--highlight">
            {tag}
          </span>
        ))}
      </div>
    </Card>
  )
}
