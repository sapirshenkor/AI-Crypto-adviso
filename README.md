# AI Crypto Advisor

A personalized crypto investor dashboard.

## Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI
- **Database:** PostgreSQL (planned)
- **Auth:** JWT (planned)
- **AI:** OpenRouter — used only for "AI Insight of the Day"
- **Prices:** CoinGecko (planned)
- **News:** NewsData.io with static fallback (planned)

## Architecture

The AI does not control the whole dashboard. News, prices, memes, layout, and feedback are rule-based. AI is used only for the daily insight.

## Project Structure

```text
ai-crypto-advisor/
  backend/     # FastAPI API
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

API runs at `http://localhost:8000`.

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
2. DB models and migrations
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
