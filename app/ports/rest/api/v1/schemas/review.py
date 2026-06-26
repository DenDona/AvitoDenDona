from datetime import datetime

from pydantic import Field

from app.ports.rest.api.v1.schema import BaseSchema


class ReviewCreateSchema(BaseSchema):
    rating: int = Field(ge=1, le=5)
    text: str | None = None


class ReviewResponseSchema(BaseSchema):
    id: int
    from_user_id: int
    to_user_id: int
    rating: int
    text: str | None
    created_at: datetime


class UserRatingSummarySchema(BaseSchema):
    to_user_id: int
    average_rating: float
    total_reviews: int