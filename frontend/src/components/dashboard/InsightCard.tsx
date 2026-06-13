import { Card } from '../ui/Card'
import type { FeedbackItemType, FeedbackVoteValue } from '../../types/feedback'
import type { AIInsightItem } from '../../types/dashboard'
import { VoteButtons } from './VoteButtons'

interface InsightCardProps {
  insight: AIInsightItem
  getVote: (itemType: FeedbackItemType, itemId: string) => FeedbackVoteValue | null
  onVote: (
    itemType: FeedbackItemType,
    itemId: string,
    tags: string[],
    vote: FeedbackVoteValue,
  ) => void
  votingDisabled?: boolean
}

export function InsightCard({
  insight,
  getVote,
  onVote,
  votingDisabled = false,
}: InsightCardProps) {
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
      <VoteButtons
        itemId={insight.id}
        itemType="ai_insight"
        currentVote={getVote('ai_insight', insight.id)}
        onVote={(vote) => onVote('ai_insight', insight.id, insight.tags, vote)}
        disabled={votingDisabled}
      />
    </Card>
  )
}
