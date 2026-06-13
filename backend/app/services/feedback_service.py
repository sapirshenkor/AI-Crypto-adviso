from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.models.user import User
from app.schemas.feedback import FeedbackSubmitRequest, FeedbackVoteSummary


def upsert_vote(
    db: Session,
    user: User,
    payload: FeedbackSubmitRequest,
) -> Feedback:
    """Create or update a vote for (user_id, item_id, item_type)."""
    existing = db.scalar(
        select(Feedback).where(
            Feedback.user_id == user.id,
            Feedback.item_id == payload.item_id,
            Feedback.item_type == payload.item_type,
        )
    )

    if existing is None:
        feedback = Feedback(
            user_id=user.id,
            item_id=payload.item_id,
            item_type=payload.item_type,
            tags=payload.tags,
            vote=payload.vote,
        )
        db.add(feedback)
    else:
        existing.vote = payload.vote
        existing.tags = payload.tags
        feedback = existing

    db.commit()
    db.refresh(feedback)
    return feedback


def get_user_votes(db: Session, user: User) -> list[FeedbackVoteSummary]:
    rows = db.scalars(
        select(Feedback).where(Feedback.user_id == user.id).order_by(Feedback.created_at.desc())
    ).all()
    return [
        FeedbackVoteSummary(
            item_id=row.item_id,
            item_type=row.item_type,
            vote=row.vote,
        )
        for row in rows
    ]
