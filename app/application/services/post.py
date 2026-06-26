from collections.abc import Sequence

from app.adapters.database.repositories.post import PostRepository
from app.application.dto.post import PostCreateDTO, PostResponseDTO, PostUpdateDTO, ExistsParamsDTO, PostFilterDTO
from app.application.dto.user import UserResponseDTO
from app.application.enums.user_role import UserRole
from app.cammon.exceptions import (
    PermissionDeniedException,
    EntityNotFoundException,
)


class PostService:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    async def create(self, post_dto: PostCreateDTO) -> PostResponseDTO:
        return await self._repository.create(post_dto=post_dto)

    async def update_by_id(self, post_id: int, post_dto: PostUpdateDTO, user: UserResponseDTO) -> PostResponseDTO:
        if not await self._repository.exists(params=ExistsParamsDTO(id=post_id)):
            raise EntityNotFoundException("post", post_id)
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            if not await self._repository.check_owner(post_id, user):
                raise PermissionDeniedException
        await self._repository.update_by_id(post_dto=post_dto, post_id=post_id)
        return await self._repository.fetch_by_id(post_id=post_id)

    async def fetch_by_id(self, post_id: int) -> PostResponseDTO:
        if not await self._repository.exists(params=ExistsParamsDTO(id=post_id)):
            raise EntityNotFoundException("post", post_id)
        return await self._repository.fetch_by_id(post_id=post_id)

    async def fetch_list(self, user: UserResponseDTO) -> Sequence[PostResponseDTO]:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            raise PermissionDeniedException
        return await self._repository.fetch_list()

    async def fetch_list_as_user(self, filters: PostFilterDTO) -> tuple[Sequence[PostResponseDTO], int]:
        return await self._repository.fetch_list_as_user(filters=filters)

    async def delete_soft(self, post_id: int, user: UserResponseDTO) -> None:
        if not await self._repository.exists(params=ExistsParamsDTO(id=post_id)):
            raise EntityNotFoundException("post", post_id)
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            if not await self._repository.check_owner(post_id, user):
                raise PermissionDeniedException
        await self._repository.delete_soft(post_id=post_id, user_id=user.id)