from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Get personalized dashboard",
    description=(
        "Returns a personalized dashboard from external providers with static fallbacks. "
        "Requires a valid Bearer JWT. Users without completed onboarding receive "
        "a safe default dashboard."
    ),
)
def read_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DashboardResponse:
    return dashboard_service.build_dashboard(db, current_user)
