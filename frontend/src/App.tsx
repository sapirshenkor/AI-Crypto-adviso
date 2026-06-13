import { Navigate, Route, Routes } from 'react-router-dom'

import { ProtectedRoute } from './components/routing/ProtectedRoute'
import { Loader } from './components/ui/Loader'
import { useAuth } from './hooks/useAuth'
import { DashboardPage } from './pages/DashboardPage'
import { LoginPage } from './pages/LoginPage'
import { OnboardingPage } from './pages/OnboardingPage'
import { SignupPage } from './pages/SignupPage'

function RootRedirect() {
  const { isAuthenticated, isLoading, onboardingCompleted } = useAuth()

  if (isLoading) {
    return <Loader message="Checking your session..." />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <Navigate to={onboardingCompleted ? '/dashboard' : '/onboarding'} replace />
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<RootRedirect />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />

      <Route element={<ProtectedRoute requireOnboardingComplete={false} />}>
        <Route path="/onboarding" element={<OnboardingPage />} />
      </Route>

      <Route element={<ProtectedRoute requireOnboardingComplete />}>
        <Route path="/dashboard" element={<DashboardPage />} />
      </Route>

      <Route path="*" element={<RootRedirect />} />
    </Routes>
  )
}
