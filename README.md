# AI Crypto Advisor

A personalized crypto investor dashboard.

## Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Auth:** JWT
- **AI:** OpenRouter — used only for "AI Insight of the Day"
- **Prices:** CoinGecko (planned)
- **News:** NewsData.io with static fallback (planned)

## Architecture

The AI does not control the whole dashboard. News, prices, memes, layout, and feedback are rule-based. AI is used only for the daily insight.

## Project Structure

```text
AI-Crypto-advisor/
  .env.example # Environment template (copy to .env at project root)
  backend/     # FastAPI API, Alembic migrations
  frontend/    # React + Vite app
  README.md
  .gitignore
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy the environment file once at the project root (see Database section below).

API runs at `http://localhost:8000`.

### Database

Requires a local PostgreSQL instance.

1. Create the database:

```sql
CREATE DATABASE ai_crypto_advisor;
```

2. Copy environment config to the project root and set your connection string:

```bash
# from project root
cp .env.example .env
```

On Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

Example variables in `project/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ai_crypto_advisor
JWT_SECRET_KEY=change-this-secret-in-development
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

3. Run migrations:

```bash
cd backend
alembic upgrade head
```

4. Verify tables exist (optional):

```bash
psql -U postgres -d ai_crypto_advisor -c "\dt"
```

Expected tables: `users`, `user_preferences`, `feedback`, `ai_insights`, `alembic_version`.

The health endpoint does not require PostgreSQL to be running.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

On Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

App runs at `http://localhost:5173`.

The Vite dev server proxies `/api` to `http://127.0.0.1:8000`, so start the backend first.

#### Frontend routes

| Route | Page | Access |
|-------|------|--------|
| `/login` | Login | Public |
| `/signup` | Signup | Public |
| `/onboarding` | Onboarding questionnaire | Authenticated, onboarding incomplete |
| `/dashboard` | Personalized dashboard | Authenticated, onboarding complete |

#### Manual frontend test flow

1. Start backend (`uvicorn app.main:app --reload`) and frontend (`npm run dev`).
2. Open `http://localhost:5173` — you should land on login.
3. Sign up or log in — JWT is stored in `localStorage`.
4. Complete onboarding — options load from the backend API.
5. Dashboard shows news, prices, AI insight, and meme sections.
6. Refresh the page — session should persist and route correctly.

### Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "AI Crypto Advisor API"
}
```

Interactive API docs: `http://localhost:8000/docs`

### Authentication

Auth endpoints:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/signup` | Register (name, email, password) |
| POST | `/api/auth/login` | Log in and receive a JWT |
| GET | `/api/auth/me` | Current user (Bearer token required) |

Manual test with curl:

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"secret123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"secret123"}'

# Me (replace TOKEN with access_token from login)
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer TOKEN"
```

#### Testing auth in Swagger UI

1. Open `http://localhost:8000/docs`.
2. Expand **Auth** → **POST /api/auth/signup** or **POST /api/auth/login**.
3. Use **Try it out** with JSON body (`email`, `password`; signup also needs `name`).
4. Copy `access_token` from the login response.
5. Click **Authorize** (top right), paste the token (Swagger adds the `Bearer` prefix), then **Authorize**.
6. Call **GET /api/auth/me** — it should return the current user without `password_hash`.

### Onboarding

Onboarding endpoints (all require Bearer token):

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/onboarding/options` | Allowed questionnaire choices |
| GET | `/api/onboarding/preferences` | Current user's saved preferences (or empty default) |
| PUT | `/api/onboarding/preferences` | Create or update preferences |

Manual test with curl:

```bash
# Options (replace TOKEN with access_token from login)
curl http://localhost:8000/api/onboarding/options \
  -H "Authorization: Bearer TOKEN"

# Get preferences (empty default if not yet saved)
curl http://localhost:8000/api/onboarding/preferences \
  -H "Authorization: Bearer TOKEN"

# Save preferences
curl -X PUT http://localhost:8000/api/onboarding/preferences \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"assets":["bitcoin","ethereum"],"investor_type":"hodler","content_types":["market_news","fun"]}'
```

#### Testing onboarding in Swagger UI

1. Log in via **Auth** → **POST /api/auth/login** and copy `access_token`.
2. Click **Authorize**, paste the token, then **Authorize**.
3. Expand **Onboarding** and try:
   - **GET /api/onboarding/options** — static choices
   - **GET /api/onboarding/preferences** — default empty state before first save
   - **PUT /api/onboarding/preferences** — valid JSON body with at least one asset and content type
4. Call **GET /api/onboarding/preferences** again to confirm saved values.

### Dashboard

Dashboard endpoint (Bearer token required):

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/dashboard` | Personalized dashboard (news, prices, AI insight, meme) |

The dashboard contract is stable for the frontend. Provider sources:

| Section | Provider | Fallback |
|---------|----------|----------|
| `news` | NewsData.io | Static news |
| `prices` | CoinGecko | Static prices |
| `ai_insight` | OpenRouter (primary → fallback model) | Static insight |
| `meme` | Local files in `backend/static/memes/` | Static meme |

Meme images are served from `GET /static/memes/{filename}`.

### External API Environment Variables

Add these to the project root `.env` (see `.env.example`):

```env
NEWS_DATA_API_KEY=
COINGECKO_DEMO_API_KEY=
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-oss-120b:free
OPENROUTER_FALLBACK_MODEL=google/gemma-4-26b-a4b-it:free
COINGECKO_API_BASE_URL=https://api.coingecko.com/api/v3
NEWS_DATA_API_BASE_URL=https://newsdata.io/api/1
OPENROUTER_API_BASE_URL=https://openrouter.ai/api/v1
BACKEND_PUBLIC_URL=http://localhost:8000
EXTERNAL_API_TIMEOUT_SECONDS=8
```

If a provider fails or returns invalid/empty data, the dashboard falls back to static content while preserving the same response shape.

Manual test with curl:

```bash
# Dashboard (replace TOKEN with access_token from login)
curl http://localhost:8000/api/dashboard \
  -H "Authorization: Bearer TOKEN"
```

#### Testing dashboard in Swagger UI

1. Log in via **Auth** → **POST /api/auth/login** and copy `access_token`.
2. Click **Authorize**, paste the token, then **Authorize**.
3. Expand **Dashboard** → **GET /api/dashboard** → **Try it out**.
4. Before onboarding, the response uses a safe default (Bitcoin + Ethereum content).
5. Save preferences via **PUT /api/onboarding/preferences**, then call the dashboard again to see asset/content-based changes.

## Development Phases

1. ✅ Project structure
2. ✅ DB models and migrations
3. ✅ Backend auth
4. ✅ Onboarding preferences
5. ✅ Dashboard endpoint (static data)
6. ✅ Frontend pages
7. ✅ External API integration (dashboard providers)
8. Feedback voting
9. Polish UI
10. Deploy
11. Final README
