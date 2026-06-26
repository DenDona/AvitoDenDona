from collections.abc import Sequence

from sqlalchemy import select, insert, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.converters.category import converter_category
from app.adapters.database.tables import CategoryTable
from app.application.dto.category import CategoryCreateDTO, CategoryUpdateDTO, CategoryResponseDTO
from app.application.interfaces.category import ICategoryRepository


class CategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def exists(self, category_id: int) -> bool:
        query = select(CategoryTable).where(CategoryTable.id == category_id, CategoryTable.deleted_at.is_(None))
        result = await self.__session.execute(query)
        return result.scalar() is not None

    async def create(self, dto: CategoryCreateDTO) -> CategoryResponseDTO:
        stmt = (
            insert(CategoryTable).values(
                name=dto.name,
                parent_id=dto.parent_id,
            )
        ).returning(CategoryTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_category(result=result)

    async def update_by_id(self, category_id: int, dto: CategoryUpdateDTO) -> None:
        update_values = dto.to_dict()
        stmt = (
            update(CategoryTable)
            .where(CategoryTable.id == category_id)
            .values(**update_values)
        )
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def fetch_by_id(self, category_id: int) -> CategoryResponseDTO:
        stmt = select(CategoryTable).where(CategoryTable.id == category_id)
        result = (await self.__session.scalars(stmt)).one()
        return converter_category(result=result)

    async def fetch_list(self) -> Sequence[CategoryResponseDTO]:
        stmt = (
            select(CategoryTable)
            .where(CategoryTable.deleted_at.is_(None))
            .order_by(CategoryTable.name)
        )
        result = await self.__session.execute(stmt)
        return [converter_category(result=row) for row in result.scalars().all()]

    async def delete_soft(self, category_id: int) -> None:
        stmt = (
            update(CategoryTable)
            .where(CategoryTable.id == category_id, CategoryTable.deleted_at.is_(None))
            .values(deleted_at=func.now(), updated_at=func.now())
        )
        await self.__session.execute(stmt)
        await self.__session.commit()
