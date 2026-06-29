from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.application.dto.user import UserCreateDTO, UserResponseDTO, UserWithPasswordDTO, UserUpdateDTO


class IUserRepository(ABC):

    @abstractmethod
    async def get_by_username(self, username: str) -> UserResponseDTO | None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserResponseDTO | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserResponseDTO | None:
        pass

    @abstractmethod
    async def get_by_login(self, login: str) -> UserWithPasswordDTO | None:
        pass

    @abstractmethod
    async def create(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        pass

    @abstractmethod
    async def update_profile(self, user_id: int, dto: UserUpdateDTO) -> UserResponseDTO:
        pass

    @abstractmethod
    async def fetch_users(self) -> Sequence[UserResponseDTO]:
        pass
