export function isOnboardingEditMode(
  search: string,
  state: unknown,
): boolean {
  const params = new URLSearchParams(search)
  if (params.get('mode') === 'edit') {
    return true
  }

  if (
    typeof state === 'object' &&
    state !== null &&
    'editPreferences' in state &&
    (state as { editPreferences?: boolean }).editPreferences === true
  ) {
    return true
  }

  return false
}
