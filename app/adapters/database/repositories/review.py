from collections.abc import Sequence

from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.converters.review import converter_review
from app.adapters.database.tables import ReviewTable
from app.application.dto.review import ReviewCreateDTO, ReviewResponseDTO, UserRatingSummaryDTO


class ReviewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def already_reviewed(self, from_user_id: int, to_user_id: int) -> bool:
        stmt = select(ReviewTable).where(
            ReviewTable.from_user_id == from_user_id,
            ReviewTable.to_user_id == to_user_id,
            ReviewTable.deleted_at.is_(None),
        )
        result = await self.__session.execute(stmt)
        return result.scalar() is not None

    async def create(self, dto: ReviewCreateDTO) -> ReviewResponseDTO:
        stmt = (
            insert(ReviewTable).values(
                from_user_id=dto.from_user_id,
                to_user_id=dto.to_user_id,
                rating=dto.rating,
                text=dto.text,
            )
        ).returning(ReviewTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_review(result=result)

    async def fetch_for_user(self, to_user_id: int) -> Sequence[ReviewResponseDTO]:
        stmt = (
            select(ReviewTable)
            .where(ReviewTable.to_user_id == to_user_id, ReviewTable.deleted_at.is_(None))
            .order_by(ReviewTable.created_at.desc())
        )
        result = await self.__session.execute(stmt)
        return [converter_review(row) for row in result.scalars().all()]

    async def get_rating_summary(self, to_user_id: int) -> UserRatingSummaryDTO:
        stmt = select(
            func.avg(ReviewTable.rating).label("avg_rating"),
            func.count(ReviewTable.id).label("total"),
        ).where(ReviewTable.to_user_id == to_user_id, ReviewTable.deleted_at.is_(None))
        result = (await self.__session.execute(stmt)).one()
        return UserRatingSummaryDTO(
            to_user_id=to_user_id,
            average_rating=round(float(result.avg_rating or 0), 2),
            total_reviews=result.total,
        )