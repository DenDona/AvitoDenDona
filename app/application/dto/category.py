from dataclasses import dataclass
from datetime import datetime

from app.application.base import ToDictMixin, Unset, UNSET


@dataclass(frozen=True, kw_only=True, slots=True)
class CategoryCreateDTO(ToDictMixin):
    name: str
    parent_id: int | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class CategoryUpdateDTO(ToDictMixin):
    name: str | Unset = UNSET
    parent_id: int | None | Unset = UNSET


@dataclass(frozen=True, kw_only=True, slots=True)
class CategoryResponseDTO:
    id: int
    name: str
    parent_id: int | None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
