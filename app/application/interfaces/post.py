from abc import ABC, abstractmethod
from collections.abc import Sequence
from app.application.dto.post import PostCreateDTO, PostUpdateDTO, PostResponseDTO, ExistsParamsDTO, PostFilterDTO


class IPostRepository(ABC):

    @abstractmethod
    async def exists(self, params: ExistsParamsDTO) -> bool:
        pass

    @abstractmethod
    async def create(self, post_dto: PostCreateDTO) -> PostResponseDTO:
        pass

    @abstractmethod
    async def update_by_id(self, post_id: int, post_dto: PostUpdateDTO) -> None:
        pass

    @abstractmethod
    async def fetch_list(self) -> Sequence[PostResponseDTO]:
        pass

    @abstractmethod
    async def fetch_list_as_user(self, filters: PostFilterDTO) -> tuple[Sequence[PostResponseDTO], int]:
        pass

    @abstractmethod
    async def fetch_by_id(self, post_id: int) -> PostResponseDTO:
        pass

    @abstractmethod
    async def delete_soft(self, post_id: int, user_id: int) -> None:
        pass