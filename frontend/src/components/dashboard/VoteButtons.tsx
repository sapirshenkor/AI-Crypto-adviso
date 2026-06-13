import type { FeedbackItemType, FeedbackVoteValue } from '../../types/feedback'

interface VoteButtonsProps {
  itemId: string
  itemType: FeedbackItemType
  currentVote: FeedbackVoteValue | null
  onVote: (vote: FeedbackVoteValue) => void
  disabled?: boolean
}

export function VoteButtons({
  currentVote,
  onVote,
  disabled = false,
}: VoteButtonsProps) {
  return (
    <div className="vote-buttons">
      <button
        type="button"
        className={`vote-button${currentVote === 1 ? ' vote-button--active' : ''}`}
        aria-label="Like"
        aria-pressed={currentVote === 1}
        disabled={disabled}
        onClick={() => onVote(1)}
      >
        👍
      </button>
      <button
        type="button"
        className={`vote-button${currentVote === -1 ? ' vote-button--active' : ''}`}
        aria-label="Dislike"
        aria-pressed={currentVote === -1}
        disabled={disabled}
        onClick={() => onVote(-1)}
      >
        👎
      </button>
    </div>
  )
}
