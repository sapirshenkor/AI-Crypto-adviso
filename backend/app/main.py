from fastapi import FastAPI

from app.api.routes import auth, health
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
