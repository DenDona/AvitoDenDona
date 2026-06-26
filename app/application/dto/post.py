from dataclasses import dataclass
from datetime import datetime

from app.application.base import ToDictMixin, Unset, UNSET
from app.application.enums.post_condition import PostCondition
from app.application.enums.post_status import PostStatus


@dataclass(frozen=True, kw_only=True, slots=True)
class PostCreateDTO(ToDictMixin):
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    city: str | None = None
    condition: PostCondition | None = None
    category_id: int | None = None
    created_by_id: int


@dataclass(frozen=True, kw_only=True, slots=True)
class PostUpdateDTO(ToDictMixin):
    title: str | Unset = UNSET
    description: str | None | Unset = UNSET
    image_url: str | None | Unset = UNSET
    price: float | None | Unset = UNSET
    city: str | None | Unset = UNSET
    status: PostStatus | Unset = UNSET
    condition: PostCondition | None | Unset = UNSET
    category_id: int | None | Unset = UNSET


@dataclass(frozen=True, kw_only=True, slots=True)
class PostResponseDTO:
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    city: str | None = None
    status: PostStatus = PostStatus.ACTIVE
    condition: PostCondition | None = None
    category_id: int | None = None
    created_by_id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class ExistsParamsDTO(ToDictMixin):
    id: int | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class PostFilterDTO:
    category_id: int | None = None
    city: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    condition: PostCondition | None = None
    status: PostStatus | None = None
    q: str | None = None
    page: int = 1
    limit: int = 20