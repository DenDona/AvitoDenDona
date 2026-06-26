from enum import StrEnum
from typing import Any
from uuid import UUID

from starlette import status


class RAMSException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ErrorCode(StrEnum):
    CODE = "code"
    NOT_FOUND = "not_found"
    INVALID_DATES = "invalid_dates"


class EntityNotFoundException(RAMSException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, entity: str = "Entity", entity_id: UUID | int | None = None) -> None:
        if entity_id is None:
            super().__init__(f"{entity} not found")
        else:
            super().__init__(f"{entity} with id={entity_id} not found")


class InvalidTokenException(RAMSException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Wrong authorization token")


class ExpiredTokenException(RAMSException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Token expired")


class PermissionDeniedException(RAMSException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "You don't have permissions")


class EntityAlreadyExists(RAMSException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, entity: str | None = None, message: str | None = None) -> None:
        super().__init__(message or f"{entity if entity else 'Entity'} already exists")


class ApplicationError(RAMSException):
    def __init__(self, code: ErrorCode, *args: Any, **kwargs: Any) -> None:
        self.code = code
        super().__init__(self.code, args)

    def __str__(self) -> str:
        return self.code
