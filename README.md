# AI Crypto Advisor

A personalized crypto investor dashboard.

## Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Auth:** JWT
- **AI:** OpenRouter (primary model + fallback model) — used only for "AI Insight of the Day"
- **Prices:** CoinGecko with static fallback
- **News:** NewsData.io with static fallback

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
6. Click **Edit preferences** — update onboarding choices and save.
7. Click **Refresh dashboard** — content reloads from the backend.
8. Vote on news articles, the AI insight, and the meme (👍 / 👎). Price cards do not have voting.
9. Refresh the page — session should persist, routing should remain correct, and previous votes should stay highlighted.

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

### Feedback

Feedback endpoints (Bearer token required):

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/feedback` | Submit or update a vote on dashboard content |
| GET | `/api/feedback/my-votes` | List the current user's saved votes |

Valid `item_type` values:

- `news`
- `ai_insight`
- `meme`

Valid `vote` values:

- `1` = like
- `-1` = dislike

Coin prices are intentionally **not** votable.

Submitting a vote for the same `(user_id, item_id, item_type)` updates the existing row (UPSERT). Feedback uniqueness is enforced logically in the service layer by `(user_id, item_id, item_type)`. No DB unique index was added in this phase.

Example request:

```json
{
  "item_id": "news_bitcoin_1",
  "item_type": "news",
  "tags": ["bitcoin", "market_news"],
  "vote": 1
}
```

Manual test with curl:

```bash
# Submit or update a vote (replace TOKEN with access_token from login)
curl -X POST http://localhost:8000/api/feedback \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"item_id":"news_bitcoin_1","item_type":"news","tags":["bitcoin"],"vote":1}'

# Get current user's votes
curl http://localhost:8000/api/feedback/my-votes \
  -H "Authorization: Bearer TOKEN"
```

#### Testing feedback in Swagger UI

1. Log in via **Auth** → **POST /api/auth/login** and copy `access_token`.
2. Click **Authorize**, paste the token, then **Authorize**.
3. Expand **Feedback** → **POST /api/feedback** → submit a vote for a dashboard item.
4. Call **GET /api/feedback/my-votes** to confirm the saved vote.
5. Submit the same item again with the opposite vote — the existing row should update, not duplicate.

## Deployment Notes

Target hosting:

- **Frontend:** Vercel
- **Backend:** Render
- **Database:** Neon PostgreSQL

Backend start command on Render:

```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Production checklist:

- Set `DATABASE_URL` to the Neon connection string (use the `postgresql+psycopg://` driver format; add `?sslmode=require` if Neon requires SSL).
- Set a strong `JWT_SECRET_KEY`.
- Configure **CORS** on the backend for the deployed Vercel frontend URL.
- Set `VITE_API_URL` on Vercel to the deployed backend URL (for example `https://your-api.onrender.com`).
- Set `BACKEND_PUBLIC_URL` on Render to the same deployed backend URL so meme image URLs resolve correctly.
- Add external API keys (`NEWS_DATA_API_KEY`, `COINGECKO_DEMO_API_KEY`, `OPENROUTER_API_KEY`) in the Render environment.

## Development Phases

1. ✅ Project structure
2. ✅ DB models and migrations
3. ✅ Backend auth
4. ✅ Onboarding preferences
5. ✅ Dashboard endpoint (static data)
6. ✅ Frontend pages
7. ✅ External API integration (dashboard providers)
8. ✅ Feedback voting
9. ✅ Polish UI
10. Deploy
11. Final README
