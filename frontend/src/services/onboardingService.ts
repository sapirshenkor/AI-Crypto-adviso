import type {
  OnboardingOptions,
  OnboardingPreferencesUpdate,
  UserPreferences,
} from '../types/onboarding'
import apiClient from './apiClient'

export async function getOptions(): Promise<OnboardingOptions> {
  const response = await apiClient.get<OnboardingOptions>(
    '/api/onboarding/options',
  )
  return response.data
}

export async function getPreferences(): Promise<UserPreferences> {
  const response = await apiClient.get<UserPreferences>(
    '/api/onboarding/preferences',
  )
  return response.data
}

export async function savePreferences(
  payload: OnboardingPreferencesUpdate,
): Promise<UserPreferences> {
  const response = await apiClient.put<UserPreferences>(
    '/api/onboarding/preferences',
    payload,
  )
  return response.data
}
