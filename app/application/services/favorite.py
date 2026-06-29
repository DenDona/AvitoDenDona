from collections.abc import Sequence

from app.adapters.database.repositories.favorite import FavoriteRepository
from app.application.dto.favorite import FavoriteResponseDTO
from app.cammon.exceptions import EntityAlreadyExists, EntityNotFoundException


class FavoriteService:
    def __init__(self, repository: FavoriteRepository) -> None:
        self._repository = repository

    async def add(self, user_id: int, post_id: int) -> FavoriteResponseDTO:
        if await self._repository.exists(user_id=user_id, post_id=post_id):
            raise EntityAlreadyExists("Favorite")
        return await self._repository.add(user_id=user_id, post_id=post_id)

    async def remove(self, user_id: int, post_id: int) -> None:
        if not await self._repository.exists(user_id=user_id, post_id=post_id):
            raise EntityNotFoundException("Favorite")
        await self._repository.remove(user_id=user_id, post_id=post_id)

    async def fetch_by_user(self, user_id: int) -> Sequence[FavoriteResponseDTO]:
        return await self._repository.fetch_by_user(user_id=user_id)
