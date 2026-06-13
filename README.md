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
npm run dev
```

App runs at `http://localhost:5173`.

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

## Development Phases

1. ✅ Project structure
2. ✅ DB models and migrations
3. ✅ Backend auth
4. ✅ Onboarding preferences
5. Dashboard endpoint (static data)
6. Frontend pages
7. Connect frontend to backend
8. External APIs
9. OpenRouter AI insight
10. Feedback voting
11. Polish UI
12. Deploy
13. Final README
