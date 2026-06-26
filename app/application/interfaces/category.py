from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.application.dto.category import CategoryCreateDTO, CategoryUpdateDTO, CategoryResponseDTO


class ICategoryRepository(ABC):

    @abstractmethod
    async def exists(self, category_id: int) -> bool:
        pass

    @abstractmethod
    async def create(self, dto: CategoryCreateDTO) -> CategoryResponseDTO:
        pass

    @abstractmethod
    async def update_by_id(self, category_id: int, dto: CategoryUpdateDTO) -> None:
        pass

    @abstractmethod
    async def fetch_by_id(self, category_id: int) -> CategoryResponseDTO:
        pass

    @abstractmethod
    async def fetch_list(self) -> Sequence[CategoryResponseDTO]:
        pass

    @abstractmethod
    async def delete_soft(self, category_id: int) -> None:
        pass
