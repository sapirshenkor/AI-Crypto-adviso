import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

import * as authService from '../services/authService'
import * as onboardingService from '../services/onboardingService'
import type { LoginCredentials, SignupCredentials } from '../types/auth'
import {
  AUTH_UNAUTHORIZED_EVENT,
  clearStoredToken,
  getStoredToken,
  setStoredToken,
} from '../utils/tokenStorage'
import { AuthContext, type AuthContextValue } from './authContext'

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthContextValue['user']>(null)
  const [token, setToken] = useState<string | null>(getStoredToken())
  const [onboardingCompleted, setOnboardingCompleted] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  const refreshOnboardingStatus = useCallback(async () => {
    const preferences = await onboardingService.getPreferences()
    setOnboardingCompleted(preferences.onboarding_completed)
    return preferences.onboarding_completed
  }, [])

  const setOnboardingCompletedState = useCallback((completed: boolean) => {
    setOnboardingCompleted(completed)
  }, [])

  const bootstrapSession = useCallback(async () => {
    const storedToken = getStoredToken()
    if (!storedToken) {
      setUser(null)
      setToken(null)
      setOnboardingCompleted(false)
      setIsLoading(false)
      return
    }

    setToken(storedToken)

    try {
      const currentUser = await authService.getCurrentUser()
      setUser(currentUser)
      await refreshOnboardingStatus()
    } catch {
      clearStoredToken()
      setUser(null)
      setToken(null)
      setOnboardingCompleted(false)
    } finally {
      setIsLoading(false)
    }
  }, [refreshOnboardingStatus])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- one-time session bootstrap
    void bootstrapSession()
  }, [bootstrapSession])

  useEffect(() => {
    const handleUnauthorized = () => {
      setUser(null)
      setToken(null)
      setOnboardingCompleted(false)
    }

    window.addEventListener(AUTH_UNAUTHORIZED_EVENT, handleUnauthorized)
    return () => {
      window.removeEventListener(AUTH_UNAUTHORIZED_EVENT, handleUnauthorized)
    }
  }, [])

  const login = useCallback(async (credentials: LoginCredentials) => {
    const response = await authService.login(credentials)
    setStoredToken(response.access_token)
    setToken(response.access_token)

    const currentUser = await authService.getCurrentUser()
    setUser(currentUser)
    const preferences = await onboardingService.getPreferences()
    setOnboardingCompleted(preferences.onboarding_completed)
    return preferences.onboarding_completed
  }, [])

  const signup = useCallback(
    async (credentials: SignupCredentials) => {
      await authService.signup(credentials)
      return login({ email: credentials.email, password: credentials.password })
    },
    [login],
  )

  const logout = useCallback(() => {
    clearStoredToken()
    setUser(null)
    setToken(null)
    setOnboardingCompleted(false)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      onboardingCompleted,
      isLoading,
      isAuthenticated: Boolean(user && token),
      login,
      signup,
      logout,
      refreshOnboardingStatus,
      setOnboardingCompleted: setOnboardingCompletedState,
    }),
    [
      user,
      token,
      onboardingCompleted,
      isLoading,
      login,
      signup,
      logout,
      refreshOnboardingStatus,
      setOnboardingCompletedState,
    ],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
