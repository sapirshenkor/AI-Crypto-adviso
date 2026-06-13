import { Navigate, Outlet } from 'react-router-dom'

import { Loader } from '../ui/Loader'
import { useAuth } from '../../hooks/useAuth'

interface ProtectedRouteProps {
  requireOnboardingComplete?: boolean
}

export function ProtectedRoute({
  requireOnboardingComplete = false,
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, onboardingCompleted } = useAuth()

  if (isLoading) {
    return <Loader message="Checking your session..." />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (requireOnboardingComplete && !onboardingCompleted) {
    return <Navigate to="/onboarding" replace />
  }

  if (!requireOnboardingComplete && onboardingCompleted) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
