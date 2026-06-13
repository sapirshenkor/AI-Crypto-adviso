from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, dashboard, health, onboarding
from app.core.config import BACKEND_DIR, settings

app = FastAPI(title=settings.app_name)

static_dir = BACKEND_DIR / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(onboarding.router, prefix=settings.api_prefix)
app.include_router(dashboard.router, prefix=settings.api_prefix)
