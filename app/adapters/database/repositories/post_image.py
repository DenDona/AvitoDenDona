from collections.abc import Sequence

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.converters.post_image import converter_post_image
from app.adapters.database.tables import PostImageTable
from app.application.dto.post_image import PostImageCreateDTO, PostImageResponseDTO


class PostImageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, dto: PostImageCreateDTO) -> PostImageResponseDTO:
        stmt = (
            insert(PostImageTable).values(
                post_id=dto.post_id,
                url=dto.url,
                order=dto.order,
            )
        ).returning(PostImageTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_post_image(result=result)

    async def fetch_by_post(self, post_id: int) -> Sequence[PostImageResponseDTO]:
        stmt = (
            select(PostImageTable)
            .where(PostImageTable.post_id == post_id)
            .order_by(PostImageTable.order)
        )
        result = await self.__session.execute(stmt)
        return [converter_post_image(result=row) for row in result.scalars().all()]

    async def get_by_id(self, image_id: int) -> PostImageResponseDTO | None:
        stmt = select(PostImageTable).where(PostImageTable.id == image_id)
        result = await self.__session.scalar(stmt)
        return converter_post_image(result=result) if result else None

    async def delete(self, image_id: int) -> None:
        stmt = delete(PostImageTable).where(PostImageTable.id == image_id)
        await self.__session.execute(stmt)
        await self.__session.commit()