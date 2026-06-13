import { Card } from '../ui/Card'
import { EmptyState } from '../ui/EmptyState'
import type { FeedbackItemType, FeedbackVoteValue } from '../../types/feedback'
import type { NewsItem } from '../../types/dashboard'
import { VoteButtons } from './VoteButtons'

interface NewsCardProps {
  items: NewsItem[]
  getVote: (itemType: FeedbackItemType, itemId: string) => FeedbackVoteValue | null
  onVote: (
    itemType: FeedbackItemType,
    itemId: string,
    tags: string[],
    vote: FeedbackVoteValue,
  ) => void
  votingDisabled?: boolean
}

export function NewsCard({
  items,
  getVote,
  onVote,
  votingDisabled = false,
}: NewsCardProps) {
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
              <VoteButtons
                itemId={item.id}
                itemType="news"
                currentVote={getVote('news', item.id)}
                onVote={(vote) => onVote('news', item.id, item.tags, vote)}
                disabled={votingDisabled}
              />
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}
