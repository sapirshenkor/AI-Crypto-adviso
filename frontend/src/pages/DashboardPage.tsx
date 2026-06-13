import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import { InsightCard } from '../components/dashboard/InsightCard'
import { MemeCard } from '../components/dashboard/MemeCard'
import { NewsCard } from '../components/dashboard/NewsCard'
import { PriceCard } from '../components/dashboard/PriceCard'
import { Button } from '../components/ui/Button'
import { Loader } from '../components/ui/Loader'
import { useAuth } from '../hooks/useAuth'
import * as dashboardService from '../services/dashboardService'
import type { DashboardResponse } from '../types/dashboard'
import { getErrorMessage } from '../utils/getErrorMessage'

export function DashboardPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuth()
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadDashboard = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await dashboardService.getDashboard()
      setDashboard(data)
    } catch (loadError: unknown) {
      setError(
        getErrorMessage(loadError, 'Could not load dashboard. Please try again.'),
      )
      setDashboard(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- refetch on dashboard navigation
    void loadDashboard()
  }, [location.key])

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
          <div className="dashboard-grid">
            <NewsCard items={dashboard.news} />
            <PriceCard items={dashboard.prices} />
            <InsightCard insight={dashboard.ai_insight} />
            <MemeCard meme={dashboard.meme} />
          </div>
        )}
      </div>
    </div>
  )
}
