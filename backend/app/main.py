from fastapi import FastAPI

from app.api.routes import auth, dashboard, health, onboarding
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(onboarding.router, prefix=settings.api_prefix)
app.include_router(dashboard.router, prefix=settings.api_prefix)
