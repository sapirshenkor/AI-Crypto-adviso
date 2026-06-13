export interface OptionItem {
  id: string
  label: string
}

export interface OnboardingOptions {
  assets: OptionItem[]
  investor_types: OptionItem[]
  content_types: OptionItem[]
}

export interface UserPreferences {
  assets: string[]
  investor_type: string | null
  content_types: string[]
  onboarding_completed: boolean
}

export interface OnboardingPreferencesUpdate {
  assets: string[]
  investor_type: string
  content_types: string[]
}
