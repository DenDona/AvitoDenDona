from collections.abc import Sequence

from app.adapters.database.repositories.post import PostRepository
from app.adapters.database.repositories.post_image import PostImageRepository
from app.application.dto.post_image import PostImageCreateDTO, PostImageResponseDTO
from app.application.dto.user import UserResponseDTO
from app.application.enums.user_role import UserRole
from app.cammon.exceptions import EntityNotFoundException, PermissionDeniedException


class PostImageService:
    def __init__(self, repository: PostImageRepository, post_repository: PostRepository) -> None:
        self._repository = repository
        self._post_repository = post_repository

    async def add(self, post_id: int, url: str, order: int, user: UserResponseDTO) -> PostImageResponseDTO:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            if not await self._post_repository.check_owner(post_id, user):
                raise PermissionDeniedException
        dto = PostImageCreateDTO(post_id=post_id, url=url, order=order)
        return await self._repository.add(dto=dto)

    async def fetch_by_post(self, post_id: int) -> Sequence[PostImageResponseDTO]:
        return await self._repository.fetch_by_post(post_id=post_id)

    async def delete(self, image_id: int, user: UserResponseDTO) -> None:
        image = await self._repository.get_by_id(image_id)
        if image is None:
            raise EntityNotFoundException(entity="PostImage", entity_id=image_id)
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            if not await self._post_repository.check_owner(image.post_id, user):
                raise PermissionDeniedException
        await self._repository.delete(image_id=image_id)