from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class FavoriteResponseDTO:
    id: int
    user_id: int
    post_id: int
    created_at: datetime
