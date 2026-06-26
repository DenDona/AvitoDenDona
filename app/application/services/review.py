from collections.abc import Sequence

from app.adapters.database.repositories.review import ReviewRepository
from app.application.dto.review import ReviewCreateDTO, ReviewResponseDTO, UserRatingSummaryDTO
from app.application.dto.user import UserResponseDTO
from app.cammon.exceptions import EntityAlreadyExists, PermissionDeniedException


class ReviewService:
    def __init__(self, repository: ReviewRepository) -> None:
        self._repository = repository

    async def create(self, to_user_id: int, rating: int, text: str | None, user: UserResponseDTO) -> ReviewResponseDTO:
        if user.id == to_user_id:
            raise PermissionDeniedException("Cannot review yourself")
        if await self._repository.already_reviewed(from_user_id=user.id, to_user_id=to_user_id):
            raise EntityAlreadyExists("Review")
        dto = ReviewCreateDTO(from_user_id=user.id, to_user_id=to_user_id, rating=rating, text=text)
        return await self._repository.create(dto=dto)

    async def fetch_for_user(self, to_user_id: int) -> Sequence[ReviewResponseDTO]:
        return await self._repository.fetch_for_user(to_user_id=to_user_id)

    async def get_rating_summary(self, to_user_id: int) -> UserRatingSummaryDTO:
        return await self._repository.get_rating_summary(to_user_id=to_user_id)