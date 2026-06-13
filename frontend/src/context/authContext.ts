import { createContext } from 'react'

import type { AuthUser, LoginCredentials, SignupCredentials } from '../types/auth'

export interface AuthContextValue {
  user: AuthUser | null
  token: string | null
  onboardingCompleted: boolean
  isLoading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<boolean>
  signup: (credentials: SignupCredentials) => Promise<boolean>
  logout: () => void
  refreshOnboardingStatus: () => Promise<boolean>
  setOnboardingCompleted: (completed: boolean) => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)
