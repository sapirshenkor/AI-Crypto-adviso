import { useCallback, useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import { InsightCard } from '../components/dashboard/InsightCard'
import { MemeCard } from '../components/dashboard/MemeCard'
import { NewsCard } from '../components/dashboard/NewsCard'
import { PriceCard } from '../components/dashboard/PriceCard'
import { Button } from '../components/ui/Button'
import { Loader } from '../components/ui/Loader'
import { useAuth } from '../hooks/useAuth'
import * as dashboardService from '../services/dashboardService'
import * as feedbackService from '../services/feedbackService'
import type { DashboardResponse } from '../types/dashboard'
import type {
  FeedbackItemType,
  FeedbackVoteSummary,
  FeedbackVoteValue,
} from '../types/feedback'
import { voteKey } from '../types/feedback'
import { getErrorMessage } from '../utils/getErrorMessage'

function buildVoteMap(votes: FeedbackVoteSummary[]): Map<string, FeedbackVoteValue> {
  return new Map(votes.map((vote) => [voteKey(vote.item_type, vote.item_id), vote.vote]))
}

export function DashboardPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuth()
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null)
  const [voteMap, setVoteMap] = useState<Map<string, FeedbackVoteValue>>(new Map())
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [voteError, setVoteError] = useState('')
  const [submittingVoteKey, setSubmittingVoteKey] = useState<string | null>(null)

  const loadDashboard = async () => {
    setLoading(true)
    setError('')
    setVoteError('')
    try {
      const [dashboardData, votes] = await Promise.all([
        dashboardService.getDashboard(),
        feedbackService.getMyVotes().catch(() => [] as FeedbackVoteSummary[]),
      ])
      setDashboard(dashboardData)
      setVoteMap(buildVoteMap(votes))
    } catch (loadError: unknown) {
      setError(
        getErrorMessage(loadError, 'Could not load dashboard. Please try again.'),
      )
      setDashboard(null)
      setVoteMap(new Map())
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- refetch on dashboard navigation
    void loadDashboard()
  }, [location.key])

  const getVote = useCallback(
    (itemType: FeedbackItemType, itemId: string): FeedbackVoteValue | null => {
      return voteMap.get(voteKey(itemType, itemId)) ?? null
    },
    [voteMap],
  )

  const handleVote = async (
    itemType: FeedbackItemType,
    itemId: string,
    tags: string[],
    vote: FeedbackVoteValue,
  ) => {
    const key = voteKey(itemType, itemId)
    const previousVote = voteMap.get(key) ?? null

    setVoteError('')
    setSubmittingVoteKey(key)
    setVoteMap((current) => {
      const next = new Map(current)
      next.set(key, vote)
      return next
    })

    try {
      await feedbackService.submitVote({
        item_id: itemId,
        item_type: itemType,
        tags,
        vote,
      })
    } catch (submitError: unknown) {
      setVoteMap((current) => {
        const next = new Map(current)
        if (previousVote === null) {
          next.delete(key)
        } else {
          next.set(key, previousVote)
        }
        return next
      })
      setVoteError(
        getErrorMessage(submitError, 'Could not save your vote. Please try again.'),
      )
    } finally {
      setSubmittingVoteKey(null)
    }
  }

  const handleEditPreferences = () => {
    navigate('/onboarding?mode=edit', { state: { editPreferences: true } })
  }

  return (
    <div className="page-shell">
      <div className="page-shell__content dashboard-page">
        <header className="dashboard-header">
          <div>
            <p className="dashboard-header__eyebrow">AI Crypto Advisor</p>
            <h1 className="page-title">Your Dashboard</h1>
            {user && (
              <p className="page-subtitle">Welcome back, {user.name}</p>
            )}
          </div>
          <div className="dashboard-header__actions">
            <Button variant="secondary" onClick={handleEditPreferences}>
              Edit preferences
            </Button>
            <Button
              variant="secondary"
              onClick={() => void loadDashboard()}
              disabled={loading}
            >
              Refresh dashboard
            </Button>
            <Button variant="secondary" onClick={logout}>
              Log out
            </Button>
          </div>
        </header>

        {loading && <Loader message="Loading your dashboard..." />}

        {!loading && error && (
          <div className="dashboard-error">
            <p className="form-error">{error}</p>
            <Button onClick={() => void loadDashboard()}>Try again</Button>
          </div>
        )}

        {!loading && !error && dashboard && (
          <>
            {voteError && (
              <p className="form-error dashboard-vote-error" role="alert">
                {voteError}
              </p>
            )}
            <div className="dashboard-grid">
              <NewsCard
                items={dashboard.news}
                getVote={getVote}
                onVote={(itemType, itemId, tags, vote) =>
                  void handleVote(itemType, itemId, tags, vote)
                }
                votingDisabled={submittingVoteKey !== null}
              />
              <PriceCard items={dashboard.prices} />
              <InsightCard
                insight={dashboard.ai_insight}
                getVote={getVote}
                onVote={(itemType, itemId, tags, vote) =>
                  void handleVote(itemType, itemId, tags, vote)
                }
                votingDisabled={submittingVoteKey !== null}
              />
              <MemeCard
                meme={dashboard.meme}
                getVote={getVote}
                onVote={(itemType, itemId, tags, vote) =>
                  void handleVote(itemType, itemId, tags, vote)
                }
                votingDisabled={submittingVoteKey !== null}
              />
            </div>
          </>
        )}
      </div>
    </div>
  )
}
