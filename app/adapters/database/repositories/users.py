from typing import Sequence

from sqlalchemy import or_, select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.converters.users import converter_user, converter_user_with_password
from app.adapters.database.tables import UserTable
from app.application.dto.user import UserCreateDTO, UserResponseDTO, UserWithPasswordDTO, UserUpdateDTO
from app.application.interfaces.auth import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_by_username(self, username: str) -> UserResponseDTO | None:
        stmt = select(UserTable).where(UserTable.username == username)
        result = await self.__session.scalar(stmt)
        return converter_user(result) if result else None

    async def get_by_email(self, email: str) -> UserResponseDTO | None:
        stmt = select(UserTable).where(UserTable.email == email)
        result = await self.__session.scalar(stmt)
        return converter_user(result) if result else None

    async def get_by_id(self, user_id: int) -> UserResponseDTO | None:
        stmt = select(UserTable).where(UserTable.id == user_id)
        result = await self.__session.scalar(stmt)
        return converter_user(result) if result else None

    async def get_by_login(self, login: str) -> UserWithPasswordDTO | None:
        stmt = select(UserTable).where(or_(UserTable.username == login, UserTable.email == login))
        result = await self.__session.scalar(stmt)
        return converter_user_with_password(result) if result else None

    async def create(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        stmt = (
            insert(UserTable).values(
                username=user_dto.username,
                email=user_dto.email,
                hashed_password=user_dto.hashed_password,
            )
        ).returning(UserTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_user(result)

    async def update_profile(self, user_id: int, dto: UserUpdateDTO) -> UserResponseDTO:
        update_values = dto.to_dict()
        stmt = (
            update(UserTable)
            .where(UserTable.id == user_id)
            .values(**update_values)
        ).returning(UserTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_user(result)

    async def fetch_users(self) -> Sequence[UserResponseDTO]:
        stmt = select(UserTable)
        result = await self.__session.execute(stmt)
        users = result.scalars().all()
        return [converter_user(result=user) for user in users]