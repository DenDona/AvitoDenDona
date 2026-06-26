import base64
import hashlib
import hmac
import os
from datetime import UTC, datetime, timedelta

import jwt

from app.adapters.database.repositories.users import UserRepository
from app.application.dto.user import UserCreateDTO, UserResponseDTO
from app.cammon.exceptions import (
    EntityAlreadyExists,
    EntityNotFoundException,
    ExpiredTokenException,
    InvalidTokenException,
    PermissionDeniedException,
)
from app.config import settings


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def register(self, username: str, password: str, email: str | None = None) -> UserResponseDTO:
        if await self._repository.get_by_username(username):
            raise EntityAlreadyExists(entity="Username")
        if email and await self._repository.get_by_email(email):
            raise EntityAlreadyExists(entity="Email")

        hashed_password = self._hash_password(password)
        return await self._repository.create(
            UserCreateDTO(username=username, email=email, hashed_password=hashed_password)
        )

    async def login(self, login: str, password: str) -> str:
        user = await self._repository.get_by_login(login)
        if user is None or not self._verify_password(password, user.hashed_password):
            raise PermissionDeniedException("Invalid login or password")
        return self._create_access_token(user_id=user.id, username=user.username)

    async def get_user_from_token(self, token: str) -> UserResponseDTO:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            user_id = payload.get("sub")
            if not user_id:
                raise InvalidTokenException("Неверный токен: отсутствует user_id")
            user_id = int(user_id)
        except jwt.ExpiredSignatureError as exc:
            raise ExpiredTokenException() from exc
        except (jwt.PyJWTError, TypeError, ValueError) as exc:
            raise InvalidTokenException() from exc

        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise EntityNotFoundException(entity="User", entity_id=user_id)
        return user

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
        return f"{base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"

    @staticmethod
    def _verify_password(password: str, hashed_password: str) -> bool:
        try:
            salt_b64, digest_b64 = hashed_password.split("$", maxsplit=1)
            salt = base64.b64decode(salt_b64.encode())
            expected_digest = base64.b64decode(digest_b64.encode())
        except (ValueError, TypeError):
            return False

        calculated_digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
        return hmac.compare_digest(expected_digest, calculated_digest)

    @staticmethod
    def _create_access_token(user_id: int, username: str) -> str:
        expire_at = datetime.now(UTC) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        payload = {
            "sub": str(user_id),
            "username": username,
            "exp": expire_at,
            "type": "access",
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
