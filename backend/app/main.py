from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, dashboard, feedback, health, onboarding
from app.core.config import BACKEND_DIR, settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-crypto-advisor-eta.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = BACKEND_DIR / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(onboarding.router, prefix=settings.api_prefix)
app.include_router(dashboard.router, prefix=settings.api_prefix)
app.include_router(feedback.router, prefix=settings.api_prefix)
