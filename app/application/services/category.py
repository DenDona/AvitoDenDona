from collections.abc import Sequence

from app.adapters.database.repositories.category import CategoryRepository
from app.application.dto.category import CategoryCreateDTO, CategoryUpdateDTO, CategoryResponseDTO
from app.application.dto.user import UserResponseDTO
from app.application.enums.user_role import UserRole
from app.cammon.exceptions import EntityNotFoundException, PermissionDeniedException, EntityAlreadyExists


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self._repository = repository

    async def create(self, dto: CategoryCreateDTO, user: UserResponseDTO) -> CategoryResponseDTO:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            raise PermissionDeniedException
        return await self._repository.create(dto=dto)

    async def update_by_id(self, category_id: int, dto: CategoryUpdateDTO, user: UserResponseDTO) -> CategoryResponseDTO:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            raise PermissionDeniedException
        if not await self._repository.exists(category_id=category_id):
            raise EntityNotFoundException("Category", category_id)
        await self._repository.update_by_id(category_id=category_id, dto=dto)
        return await self._repository.fetch_by_id(category_id=category_id)

    async def fetch_by_id(self, category_id: int) -> CategoryResponseDTO:
        if not await self._repository.exists(category_id=category_id):
            raise EntityNotFoundException("Category", category_id)
        return await self._repository.fetch_by_id(category_id=category_id)

    async def fetch_list(self) -> Sequence[CategoryResponseDTO]:
        return await self._repository.fetch_list()

    async def delete_soft(self, category_id: int, user: UserResponseDTO) -> None:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            raise PermissionDeniedException
        if not await self._repository.exists(category_id=category_id):
            raise EntityNotFoundException("Category", category_id)
        await self._repository.delete_soft(category_id=category_id)
