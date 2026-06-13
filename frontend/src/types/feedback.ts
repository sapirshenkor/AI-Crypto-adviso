export type FeedbackItemType = 'news' | 'ai_insight' | 'meme'
export type FeedbackVoteValue = 1 | -1

export interface SubmitVoteRequest {
  item_id: string
  item_type: FeedbackItemType
  tags: string[]
  vote: FeedbackVoteValue
}

export interface FeedbackResponse {
  id: string
  item_id: string
  item_type: string
  tags: string[]
  vote: FeedbackVoteValue
  created_at: string
}

export interface FeedbackVoteSummary {
  item_id: string
  item_type: FeedbackItemType
  vote: FeedbackVoteValue
}

export function voteKey(itemType: FeedbackItemType, itemId: string): string {
  return `${itemType}:${itemId}`
}
