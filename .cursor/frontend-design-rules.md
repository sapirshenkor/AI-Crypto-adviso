# Frontend Design Rules — AI Crypto Advisor

You are working on the **AI Crypto Advisor** frontend.

The frontend stack is:

* React
* Vite
* TypeScript

The goal is to create a modern, clean, crypto-focused dashboard inspired by products such as CoinMarketCap, CoinGecko, Messari, and DeBank.

---

## 1. General UI Direction

The UI should feel:

* Modern
* Clean
* Professional
* Dashboard-oriented
* Crypto/finance focused
* Friendly for a home-assignment demo

Avoid overly playful, noisy, or cluttered design.

Prefer a dark SaaS/dashboard look with clear cards, strong hierarchy, and readable content.

---

## 2. Color Palette

Use this palette consistently.

```text
Background:        #0F172A
Surface:           #1E293B
Surface Elevated:  #334155

Primary:           #F7931A
Primary Hover:     #E67E00

Text Primary:      #F8FAFC
Text Secondary:    #CBD5E1
Text Muted:        #94A3B8

Border:            #334155

Success:           #22C55E
Danger:            #EF4444
Warning:           #FACC15
```

Do not introduce new colors unless explicitly approved.

---

## 3. Typography

Use a clean modern font.

Recommended:

```text
Inter
```

Typography rules:

* Page titles: large, bold, clear
* Section titles: medium-large, semibold
* Body text: readable, normal weight
* Metadata/helper text: smaller and muted
* Avoid excessive uppercase text

Suggested hierarchy:

```text
Page title:      text-3xl / font-bold
Section title:   text-xl / font-semibold
Card title:      text-lg / font-semibold
Body text:       text-sm or text-base
Muted text:      text-sm / text-slate-400
```

---

## 4. Layout Rules

Use a centered responsive layout.

Suggested max width:

```text
max-width: 1200px
```

Desktop dashboard layout:

```text
Header

Dashboard Grid

+-------------------+-------------------+
| Market News       | Coin Prices       |
+-------------------+-------------------+
| AI Insight        | Crypto Meme       |
+-------------------+-------------------+
```

Mobile layout:

```text
Market News
Coin Prices
AI Insight
Crypto Meme
```

Rules:

* Use consistent spacing.
* Prefer `gap-6` between dashboard sections.
* Use `px-4` on mobile and wider padding on desktop.
* Avoid full-width content that feels stretched.
* Keep important content above the fold when possible.

---

## 5. Cards / Sections

Each major dashboard section must be inside a reusable card.

Card style:

```text
background: Surface
border: 1px solid Border
border-radius: 16px
padding: 20px–24px
subtle shadow
```

Cards should have:

* Clear section title
* Optional subtitle/helper text
* Content area
* Optional action area, such as voting buttons

Do not create different card styles for every section.

---

## 6. Buttons

Create a reusable `Button` component.

Button variants:

### Primary

Used for main actions.

```text
background: Primary
hover: Primary Hover
text: white or near-white
border-radius: 10px–12px
font-weight: 600
```

### Secondary

Used for less important actions.

```text
background: transparent or Surface Elevated
border: 1px solid Border
text: Text Primary
```

### Danger

Used only for destructive actions.

```text
background: Danger
text: white
```

Button rules:

* Buttons should feel consistent across all pages.
* Use clear hover states.
* Use disabled states where needed.
* Avoid inline one-off button styling.
* Do not use random colors for buttons.

---

## 7. Forms

Used for login, signup, and onboarding.

Form fields should be:

```text
background: Surface
border: 1px solid Border
text: Text Primary
placeholder: Text Muted
border-radius: 10px–12px
```

Form rules:

* Labels should be clear.
* Show validation errors near the field.
* Use readable spacing between inputs.
* Avoid cramped forms.
* Login/signup pages should be centered and clean.
* Onboarding should feel like a short guided questionnaire.

---

## 8. Onboarding UI

The onboarding page should feel simple and guided.

Recommended structure:

```text
Title
Short explanation
Question sections
Submit button
```

Each question group should use card-like styling.

For selectable options:

* Use pill buttons or checkbox cards.
* Selected state should use Primary color.
* Unselected state should use Surface Elevated / Border.
* Keep labels readable and friendly.

Do not make onboarding feel like a long enterprise form.

---

## 9. Dashboard UI

Dashboard sections:

* Market News
* Coin Prices
* AI Insight of the Day
* Crypto Meme

Rules:

* Each section should be visually distinct but use the same card system.
* Show empty states clearly, for example when `news` is an empty array.
* Prices should be easy to scan.
* AI insight should feel highlighted but not exaggerated.
* Meme section should show title and image cleanly.
* Voting buttons should be visually small and consistent.

Suggested voting UI:

```text
👍 Helpful    👎 Not useful
```

Voting is not implemented yet unless explicitly requested in a later phase.

If voting UI is added before backend feedback endpoints exist, keep it disabled or mocked only if approved.

---

## 10. Component Architecture

Use TypeScript and reusable components.

Suggested structure:

```text
src/
├── pages/
│   ├── LoginPage.tsx
│   ├── SignupPage.tsx
│   ├── OnboardingPage.tsx
│   └── DashboardPage.tsx
│
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Loader.tsx
│   │   └── EmptyState.tsx
│   │
│   ├── dashboard/
│   │   ├── NewsCard.tsx
│   │   ├── PriceCard.tsx
│   │   ├── InsightCard.tsx
│   │   └── MemeCard.tsx
│
├── services/
│   ├── authService.ts
│   ├── onboardingService.ts
│   └── dashboardService.ts
│
├── types/
│   ├── auth.ts
│   ├── onboarding.ts
│   └── dashboard.ts
```

Rules:

* Keep pages focused on orchestration and layout.
* Move API calls into service files.
* Move reusable UI into components.
* Avoid large TSX files with hundreds of lines.
* Avoid duplicated markup.
* Avoid using `any`.
* Define API response types in `types/`.

---

## 11. TypeScript Rules

Frontend must be implemented using React + TypeScript.

Requirements:

* Use `.tsx` for React components.
* Use `.ts` for services, utilities, and types.
* Define types/interfaces for all API contracts.
* Avoid `any`.
* Prefer explicit types for API responses.
* Keep types close to the domain.

Required domain types:

```text
AuthUser
LoginResponse
OnboardingOptions
UserPreferences
DashboardResponse
NewsItem
PriceItem
AIInsightItem
MemeItem
```

---

## 12. API Integration Style

Do not hardcode API URLs directly inside components.

Use a shared API base URL config.

Example:

```text
VITE_API_URL
```

Rules:

* API calls belong in service files.
* Components should call services, not `fetch` directly.
* Attach JWT token consistently.
* Handle loading, error, and empty states.
* Do not expose secrets in frontend code.

---

## 13. Responsiveness

Every page must work on:

* Mobile
* Tablet
* Desktop

Rules:

* Use responsive grid/flex layouts.
* Dashboard should be two columns on desktop and one column on mobile.
* Forms should not overflow on small screens.
* Cards should remain readable on mobile.
* Avoid tiny text and cramped buttons.

---

## 14. Accessibility Basics

Follow basic accessibility practices:

* Use semantic HTML where possible.
* Buttons must be real `<button>` elements.
* Inputs must have labels.
* Interactive elements should be keyboard accessible.
* Keep color contrast readable.
* Do not rely only on color to communicate state.
* Add useful `alt` text for meme images.

---

## 15. Loading / Error / Empty States

Every API-backed page should support:

* Loading state
* Error state
* Empty state where relevant

Examples:

```text
Loading your dashboard...
Could not load dashboard. Please try again.
No market news selected yet.
```

Do not leave blank screens.

---

## 16. Design Restrictions

Do not:

* Introduce new color palettes
* Mix unrelated button styles
* Add heavy animation libraries
* Add complex charting libraries unless explicitly approved
* Add Tailwind, shadcn, Material UI, Chakra, or Bootstrap unless already installed or explicitly approved
* Change backend contracts
* Implement features from future phases without approval

---

## 17. Implementation Mindset

Build the frontend in small, clean phases.

Before coding any frontend phase:

1. Read all `.cursor/` guidance files.
2. Inspect the current frontend setup.
3. Confirm the current stack and installed dependencies.
4. Present a short implementation plan.
5. Wait for approval before coding.

# Definition of Done (Frontend)

A frontend implementation is considered complete only if:

- Uses TypeScript without `any`
- Fully responsive (mobile/tablet/desktop)
- Uses reusable UI components
- Handles loading states
- Handles error states
- Handles empty states
- Follows the shared color palette
- Follows the shared spacing system
- Matches the approved dashboard style
- Passes linting/build checks

Always preserve existing working behavior.
