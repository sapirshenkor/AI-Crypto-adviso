import { Navigate, Outlet, useLocation } from 'react-router-dom'

import { Loader } from '../ui/Loader'
import { useAuth } from '../../hooks/useAuth'
import { isOnboardingEditMode } from '../../utils/onboardingEditMode'

interface ProtectedRouteProps {
  requireOnboardingComplete?: boolean
}

export function ProtectedRoute({
  requireOnboardingComplete = false,
}: ProtectedRouteProps) {
  const location = useLocation()
  const { isAuthenticated, isLoading, onboardingCompleted } = useAuth()
  const editMode = isOnboardingEditMode(location.search, location.state)

  if (isLoading) {
    return <Loader message="Checking your session..." />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requireOnboardingComplete && !onboardingCompleted) {
    return <Navigate to="/onboarding" replace />
  }

  if (!requireOnboardingComplete && onboardingCompleted && !editMode) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
