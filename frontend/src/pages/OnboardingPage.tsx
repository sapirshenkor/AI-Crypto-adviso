import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { Loader } from '../components/ui/Loader'
import { useAuth } from '../hooks/useAuth'
import * as onboardingService from '../services/onboardingService'
import type { OnboardingOptions } from '../types/onboarding'
import { getErrorMessage } from '../utils/getErrorMessage'
import { isOnboardingEditMode } from '../utils/onboardingEditMode'

function toggleSelection(current: string[], value: string): string[] {
  return current.includes(value)
    ? current.filter((item) => item !== value)
    : [...current, value]
}

export function OnboardingPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { setOnboardingCompleted } = useAuth()
  const isEditMode = isOnboardingEditMode(location.search, location.state)
  const [options, setOptions] = useState<OnboardingOptions | null>(null)
  const [selectedAssets, setSelectedAssets] = useState<string[]>([])
  const [selectedInvestorType, setSelectedInvestorType] = useState('')
  const [selectedContentTypes, setSelectedContentTypes] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [validationError, setValidationError] = useState('')

  useEffect(() => {
    const loadOnboarding = async () => {
      try {
        const [optionsData, preferences] = await Promise.all([
          onboardingService.getOptions(),
          onboardingService.getPreferences(),
        ])
        setOptions(optionsData)

        if (preferences.onboarding_completed) {
          setSelectedAssets(preferences.assets)
          setSelectedInvestorType(preferences.investor_type ?? '')
          setSelectedContentTypes(preferences.content_types)
        }
      } catch (loadError: unknown) {
        setError(
          getErrorMessage(loadError, 'Could not load onboarding options.'),
        )
      } finally {
        setLoading(false)
      }
    }

    void loadOnboarding()
  }, [])

  const handleSubmit = async () => {
    setValidationError('')
    setError('')

    if (selectedAssets.length === 0) {
      setValidationError('Select at least one crypto asset.')
      return
    }
    if (!selectedInvestorType) {
      setValidationError('Select your investor type.')
      return
    }
    if (selectedContentTypes.length === 0) {
      setValidationError('Select at least one content type.')
      return
    }

    setSubmitting(true)
    try {
      const saved = await onboardingService.savePreferences({
        assets: selectedAssets,
        investor_type: selectedInvestorType,
        content_types: selectedContentTypes,
      })
      setOnboardingCompleted(saved.onboarding_completed)
      navigate('/dashboard', {
        replace: true,
        state: { refreshDashboard: true },
      })
    } catch (submitError: unknown) {
      setError(
        getErrorMessage(submitError, 'Could not save preferences. Please try again.'),
      )
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <Loader
        message={
          isEditMode
            ? 'Loading your preferences...'
            : 'Loading onboarding options...'
        }
      />
    )
  }

  if (error && !options) {
    return (
      <div className="page-shell">
        <div className="page-shell__content">
          <Card title="Onboarding unavailable">
            <p className="form-error">{error}</p>
          </Card>
        </div>
      </div>
    )
  }

  if (!options) {
    return null
  }

  return (
    <div className="page-shell">
      <div className="page-shell__content onboarding-page">
        <header className="onboarding-page__header">
          <h1 className="page-title">
            {isEditMode ? 'Edit your preferences' : 'Set your preferences'}
          </h1>
          <p className="page-subtitle">
            {isEditMode
              ? 'Update your interests to refresh your personalized dashboard.'
              : 'Tell us what you care about so we can personalize your dashboard.'}
          </p>
        </header>

        <Card title="What crypto assets are you interested in?">
          <div className="option-grid">
            {options.assets.map((asset) => (
              <button
                key={asset.id}
                type="button"
                className={`option-pill ${
                  selectedAssets.includes(asset.id) ? 'option-pill--selected' : ''
                }`}
                onClick={() =>
                  setSelectedAssets((current) => toggleSelection(current, asset.id))
                }
              >
                {asset.label}
              </button>
            ))}
          </div>
        </Card>

        <Card title="What type of investor are you?">
          <div className="option-grid">
            {options.investor_types.map((investorType) => (
              <button
                key={investorType.id}
                type="button"
                className={`option-pill ${
                  selectedInvestorType === investorType.id
                    ? 'option-pill--selected'
                    : ''
                }`}
                onClick={() => setSelectedInvestorType(investorType.id)}
              >
                {investorType.label}
              </button>
            ))}
          </div>
        </Card>

        <Card title="What kind of content would you like to see?">
          <div className="option-grid">
            {options.content_types.map((contentType) => (
              <button
                key={contentType.id}
                type="button"
                className={`option-pill ${
                  selectedContentTypes.includes(contentType.id)
                    ? 'option-pill--selected'
                    : ''
                }`}
                onClick={() =>
                  setSelectedContentTypes((current) =>
                    toggleSelection(current, contentType.id),
                  )
                }
              >
                {contentType.label}
              </button>
            ))}
          </div>
        </Card>

        {(validationError || error) && (
          <p className="form-error">{validationError || error}</p>
        )}

        <Button onClick={handleSubmit} disabled={submitting} fullWidth>
          {submitting
            ? 'Saving preferences...'
            : isEditMode
              ? 'Save preferences'
              : 'Continue to dashboard'}
        </Button>
      </div>
    </div>
  )
}
