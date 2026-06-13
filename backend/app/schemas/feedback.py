from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

FeedbackItemType = Literal["news", "ai_insight", "meme"]
FeedbackVoteValue = Literal[1, -1]


class FeedbackSubmitRequest(BaseModel):
    item_id: str = Field(min_length=1)
    item_type: FeedbackItemType
    tags: list[str] = Field(default_factory=list)
    vote: FeedbackVoteValue


class FeedbackResponse(BaseModel):
    id: UUID
    item_id: str
    item_type: str
    tags: list[str]
    vote: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackVoteSummary(BaseModel):
    item_id: str
    item_type: str
    vote: int

    model_config = {"from_attributes": True}
