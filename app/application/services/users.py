from collections.abc import Sequence

from app.adapters.database.repositories.users import UserRepository
from app.application.dto.user import UserResponseDTO
from app.application.enums.user_role import UserRole
from app.cammon.exceptions import PermissionDeniedException


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def fetch_users(self, user: UserResponseDTO) -> Sequence[UserResponseDTO]:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            raise PermissionDeniedException
        return await self._repository.fetch_users()