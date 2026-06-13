# AI Crypto Advisor

A personalized crypto investor dashboard.

## Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Auth:** JWT (planned)
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

Example `DATABASE_URL` in `project/.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ai_crypto_advisor
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

## Development Phases

1. ✅ Project structure
2. ✅ DB models and migrations
3. Backend auth
4. Onboarding preferences
5. Dashboard endpoint (static data)
6. Frontend pages
7. Connect frontend to backend
8. External APIs
9. OpenRouter AI insight
10. Feedback voting
11. Polish UI
12. Deploy
13. Final README
