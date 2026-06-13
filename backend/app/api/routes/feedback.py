from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.feedback import FeedbackResponse, FeedbackSubmitRequest, FeedbackVoteSummary
from app.services import feedback_service

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post(
    "",
    response_model=FeedbackResponse,
    summary="Submit or update feedback vote",
    description=(
        "Creates a new vote or updates an existing one for the authenticated user. "
        "Uniqueness is enforced logically on (user_id, item_id, item_type)."
    ),
)
def submit_feedback(
    payload: FeedbackSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FeedbackResponse:
    return feedback_service.upsert_vote(db, current_user, payload)


@router.get(
    "/my-votes",
    response_model=list[FeedbackVoteSummary],
    summary="Get current user's votes",
    description="Returns all feedback votes for the authenticated user.",
)
def read_my_votes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[FeedbackVoteSummary]:
    return feedback_service.get_user_votes(db, current_user)
