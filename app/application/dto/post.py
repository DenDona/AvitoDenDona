from dataclasses import dataclass
from datetime import datetime

from app.application.base import ToDictMixin, Unset, UNSET


@dataclass(frozen=True, kw_only=True, slots=True)
class PostCreateDTO(ToDictMixin):
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    created_by_id: int


@dataclass(frozen=True, kw_only=True, slots=True)
class PostUpdateDTO(ToDictMixin):
    title: str | Unset = UNSET
    description: str | None | Unset = UNSET
    image_url: str | None | Unset = UNSET
    price: float | None | Unset = UNSET


@dataclass(frozen=True, kw_only=True, slots=True)
class PostResponseDTO:
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    created_by_id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

@dataclass(frozen=True, kw_only=True, slots=True)
class ExistsParamsDTO(ToDictMixin):
    id: int | None = None