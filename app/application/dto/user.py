from dataclasses import dataclass
from datetime import datetime

from app.application.base import Unset, UNSET
from app.application.enums.user_role import UserRole


@dataclass(slots=True, kw_only=True)
class UserDTO:
    id: int
    role: UserRole


@dataclass(slots=True, kw_only=True)
class UserCreateDTO:
    username: str
    hashed_password: str
    email: str | None = None


@dataclass(slots=True, kw_only=True)
class UserResponseDTO:
    id: int
    username: str
    email: str | None
    role: UserRole
    created_at: datetime
    updated_at: datetime | Unset = UNSET
    deleted_at: datetime | Unset = UNSET


@dataclass(slots=True, kw_only=True)
class UserWithPasswordDTO:
    id: int
    username: str
    email: str | None
    hashed_password: str
    role: UserRole
    created_at: datetime
    updated_at: datetime | Unset = UNSET
    deleted_at: datetime | Unset = UNSET

