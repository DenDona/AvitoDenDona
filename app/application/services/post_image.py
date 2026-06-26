from collections.abc import Sequence

from app.adapters.database.repositories.post_image import PostImageRepository
from app.application.dto.post_image import PostImageCreateDTO, PostImageResponseDTO
from app.application.dto.user import UserResponseDTO
from app.application.enums.user_role import UserRole
from app.cammon.exceptions import PermissionDeniedException


class PostImageService:
    def __init__(self, repository: PostImageRepository) -> None:
        self._repository = repository

    async def add(self, post_id: int, url: str, order: int, user: UserResponseDTO) -> PostImageResponseDTO:
        dto = PostImageCreateDTO(post_id=post_id, url=url, order=order)
        return await self._repository.add(dto=dto)

    async def fetch_by_post(self, post_id: int) -> Sequence[PostImageResponseDTO]:
        return await self._repository.fetch_by_post(post_id=post_id)

    async def delete(self, image_id: int, user: UserResponseDTO) -> None:
        if user.role not in [UserRole.ADMINISTRATOR, UserRole.MODERATOR]:
            raise PermissionDeniedException
        await self._repository.delete(image_id=image_id)