import type {
  FeedbackResponse,
  FeedbackVoteSummary,
  SubmitVoteRequest,
} from '../types/feedback'
import apiClient from './apiClient'

export async function submitVote(
  payload: SubmitVoteRequest,
): Promise<FeedbackResponse> {
  const response = await apiClient.post<FeedbackResponse>(
    '/api/feedback',
    payload,
  )
  return response.data
}

export async function getMyVotes(): Promise<FeedbackVoteSummary[]> {
  const response = await apiClient.get<FeedbackVoteSummary[]>(
    '/api/feedback/my-votes',
  )
  return response.data
}
