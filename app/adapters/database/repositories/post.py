from typing import Sequence

from sqlalchemy import select, insert, update, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.converters.post import converter_post
from app.adapters.database.tables import PostTable
from app.application.dto.post import PostCreateDTO, PostResponseDTO, PostUpdateDTO, ExistsParamsDTO, PostFilterDTO
from app.application.dto.user import UserResponseDTO
from app.application.interfaces.post import IPostRepository


class PostRepository(IPostRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def exists(self, params: ExistsParamsDTO) -> bool:
        query = select(PostTable).filter_by(**params.to_dict(exclude_fields=()))
        result = await self.__session.execute(query)
        return result.scalar() is not None

    async def check_owner(self, post_id: int, user: UserResponseDTO) -> bool:
        post = await self.fetch_by_id(post_id=post_id)
        return post.created_by_id == user.id

    async def create(self, post_dto: PostCreateDTO) -> PostResponseDTO:
        stmt = (
            insert(PostTable).values(
                title=post_dto.title,
                description=post_dto.description,
                image_url=post_dto.image_url,
                price=post_dto.price,
                city=post_dto.city,
                condition=post_dto.condition,
                category_id=post_dto.category_id,
                created_by_id=post_dto.created_by_id,
            )
        ).returning(PostTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_post(result=result)

    async def update_by_id(self, post_id: int, post_dto: PostUpdateDTO) -> None:
        update_values = post_dto.to_dict()
        stmt = (
            update(PostTable)
            .where(PostTable.id == post_id)
            .values(**update_values)
        )
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def fetch_by_id(self, post_id: int) -> PostResponseDTO:
        stmt = select(PostTable).where(PostTable.id == post_id)
        result = (await self.__session.scalars(stmt)).one()
        return converter_post(result=result)

    async def fetch_list(self) -> Sequence[PostResponseDTO]:
        stmt = select(PostTable).order_by(PostTable.created_at.desc())
        result = await self.__session.execute(stmt)
        return [converter_post(result=post) for post in result.scalars().all()]

    async def fetch_list_as_user(self, filters: PostFilterDTO) -> tuple[Sequence[PostResponseDTO], int]:
        conditions = [PostTable.deleted_at.is_(None)]

        if filters.category_id is not None:
            conditions.append(PostTable.category_id == filters.category_id)
        if filters.city is not None:
            conditions.append(PostTable.city.ilike(f"%{filters.city}%"))
        if filters.min_price is not None:
            conditions.append(PostTable.price >= filters.min_price)
        if filters.max_price is not None:
            conditions.append(PostTable.price <= filters.max_price)
        if filters.condition is not None:
            conditions.append(PostTable.condition == filters.condition)
        if filters.status is not None:
            conditions.append(PostTable.status == filters.status)
        if filters.q is not None:
            conditions.append(
                or_(
                    PostTable.title.ilike(f"%{filters.q}%"),
                    PostTable.description.ilike(f"%{filters.q}%"),
                )
            )

        count_stmt = select(func.count()).select_from(PostTable).where(*conditions)
        total = (await self.__session.execute(count_stmt)).scalar_one()

        offset = (filters.page - 1) * filters.limit
        stmt = (
            select(PostTable)
            .where(*conditions)
            .order_by(PostTable.created_at.desc())
            .offset(offset)
            .limit(filters.limit)
        )
        result = await self.__session.execute(stmt)
        posts = [converter_post(result=post) for post in result.scalars().all()]
        return posts, total

    async def delete_soft(self, post_id: int, user_id: int) -> None:
        stmt = (
            update(PostTable)
            .where(
                PostTable.id == post_id,
                PostTable.created_by_id == user_id,
                PostTable.deleted_at.is_(None),
            )
            .values(deleted_at=func.now(), updated_at=func.now())
        )
        await self.__session.execute(stmt)
        await self.__session.commit()