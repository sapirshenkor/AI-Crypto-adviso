import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Loader } from '../components/ui/Loader'
import { getErrorMessage } from '../utils/getErrorMessage'
import { useAuth } from '../hooks/useAuth'

export function LoginPage() {
  const navigate = useNavigate()
  const { login, isAuthenticated, onboardingCompleted, isLoading } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if (isLoading) {
    return <Loader message="Checking your session..." />
  }

  if (isAuthenticated) {
    return (
      <Navigate to={onboardingCompleted ? '/dashboard' : '/onboarding'} replace />
    )
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)

    try {
      const completed = await login({ email, password })
      navigate(completed ? '/dashboard' : '/onboarding', { replace: true })
    } catch (submitError: unknown) {
      setError(getErrorMessage(submitError, 'Could not log in. Please try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-card__header">
          <h1 className="page-title">Welcome back</h1>
          <p className="page-subtitle">Log in to your AI Crypto Advisor dashboard</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
            required
            autoComplete="email"
          />
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter your password"
            required
            autoComplete="current-password"
          />

          {error && <p className="form-error">{error}</p>}

          <Button type="submit" fullWidth disabled={submitting}>
            {submitting ? 'Logging in...' : 'Log in'}
          </Button>
        </form>

        <p className="auth-card__footer">
          New here? <Link to="/signup">Create an account</Link>
        </p>
      </div>
    </div>
  )
}
