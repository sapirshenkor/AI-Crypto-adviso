import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Loader } from '../components/ui/Loader'
import { getErrorMessage } from '../utils/getErrorMessage'
import { useAuth } from '../hooks/useAuth'

export function SignupPage() {
  const navigate = useNavigate()
  const { signup, isAuthenticated, onboardingCompleted, isLoading } = useAuth()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [validationError, setValidationError] = useState('')
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
    setValidationError('')

    if (password !== confirmPassword) {
      setValidationError('Passwords do not match.')
      return
    }

    setSubmitting(true)

    try {
      const completed = await signup({ name, email, password })
      navigate(completed ? '/dashboard' : '/onboarding', { replace: true })
    } catch (submitError: unknown) {
      setError(
        getErrorMessage(submitError, 'Could not create account. Please try again.'),
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-card__header">
          <h1 className="page-title">Create your account</h1>
          <p className="page-subtitle">
            Start building your personalized crypto dashboard
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <Input
            label="Name"
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Your name"
            required
            autoComplete="name"
          />
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
            onChange={(event) => {
              setPassword(event.target.value)
              setValidationError('')
            }}
            placeholder="At least 8 characters"
            required
            minLength={8}
            autoComplete="new-password"
          />
          <Input
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(event) => {
              setConfirmPassword(event.target.value)
              setValidationError('')
            }}
            placeholder="Re-enter your password"
            required
            minLength={8}
            autoComplete="new-password"
            error={validationError}
          />

          {error && <p className="form-error">{error}</p>}

          <Button type="submit" fullWidth disabled={submitting}>
            {submitting ? 'Creating account...' : 'Sign up'}
          </Button>
        </form>

        <p className="auth-card__footer">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  )
}
