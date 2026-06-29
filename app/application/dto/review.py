from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class ReviewCreateDTO:
    from_user_id: int
    to_user_id: int
    rating: int
    text: str | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class ReviewResponseDTO:
    id: int
    from_user_id: int
    to_user_id: int
    rating: int
    text: str | None
    created_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UserRatingSummaryDTO:
    to_user_id: int
    average_rating: float
    total_reviews: int