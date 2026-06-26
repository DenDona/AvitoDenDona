from collections.abc import Sequence

from app.adapters.database.repositories.users import UserRepository
from app.application.dto.user import UserResponseDTO, UserUpdateDTO
from app.application.enums.user_role import UserRole
from app.cammon.exceptions import EntityNotFoundException, PermissionDeniedException


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def fetch_users(self, user: UserResponseDTO) -> Sequence[UserResponseDTO]:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            raise PermissionDeniedException
        return await self._repository.fetch_users()

    async def get_by_id(self, user_id: int) -> UserResponseDTO:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise EntityNotFoundException(entity="User", entity_id=user_id)
        return user

    async def update_profile(self, user_id: int, dto: UserUpdateDTO) -> UserResponseDTO:
        return await self._repository.update_profile(user_id=user_id, dto=dto)