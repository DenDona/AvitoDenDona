from collections.abc import Sequence

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.converters.favorite import converter_favorite
from app.adapters.database.tables import FavoriteTable
from app.application.dto.favorite import FavoriteResponseDTO


class FavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def exists(self, user_id: int, post_id: int) -> bool:
        stmt = select(FavoriteTable).where(
            FavoriteTable.user_id == user_id,
            FavoriteTable.post_id == post_id,
        )
        result = await self.__session.execute(stmt)
        return result.scalar() is not None

    async def add(self, user_id: int, post_id: int) -> FavoriteResponseDTO:
        stmt = (
            insert(FavoriteTable).values(user_id=user_id, post_id=post_id)
        ).returning(FavoriteTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_favorite(result=result)

    async def remove(self, user_id: int, post_id: int) -> None:
        stmt = delete(FavoriteTable).where(
            FavoriteTable.user_id == user_id,
            FavoriteTable.post_id == post_id,
        )
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def fetch_by_user(self, user_id: int) -> Sequence[FavoriteResponseDTO]:
        stmt = (
            select(FavoriteTable)
            .where(FavoriteTable.user_id == user_id)
            .order_by(FavoriteTable.created_at.desc())
        )
        result = await self.__session.execute(stmt)
        return [converter_favorite(result=row) for row in result.scalars().all()]