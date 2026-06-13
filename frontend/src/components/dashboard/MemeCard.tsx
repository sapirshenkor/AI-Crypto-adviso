import { Card } from '../ui/Card'
import type { FeedbackItemType, FeedbackVoteValue } from '../../types/feedback'
import type { MemeItem } from '../../types/dashboard'
import { VoteButtons } from './VoteButtons'

interface MemeCardProps {
  meme: MemeItem
  getVote: (itemType: FeedbackItemType, itemId: string) => FeedbackVoteValue | null
  onVote: (
    itemType: FeedbackItemType,
    itemId: string,
    tags: string[],
    vote: FeedbackVoteValue,
  ) => void
  votingDisabled?: boolean
}

export function MemeCard({
  meme,
  getVote,
  onVote,
  votingDisabled = false,
}: MemeCardProps) {
  return (
    <Card title="Crypto Meme" subtitle="A lighter moment from the crypto world">
      <div className="meme-card">
        <h3 className="meme-card__title">{meme.title}</h3>
        <div className="meme-card__image-wrap">
          <img
            className="meme-card__image"
            src={meme.image_url}
            alt={meme.title}
          />
        </div>
        <div className="tag-list">
          {meme.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
        <VoteButtons
          itemId={meme.id}
          itemType="meme"
          currentVote={getVote('meme', meme.id)}
          onVote={(vote) => onVote('meme', meme.id, meme.tags, vote)}
          disabled={votingDisabled}
        />
      </div>
    </Card>
  )
}
