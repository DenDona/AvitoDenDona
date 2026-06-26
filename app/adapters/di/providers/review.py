from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.repositories.review import ReviewRepository
from app.application.services.review import ReviewService


class ReviewProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def review_repository(self, session: AsyncSession) -> ReviewRepository:
        return ReviewRepository(session)

    @provide(scope=Scope.REQUEST)
    def review_service(self, repository: ReviewRepository) -> ReviewService:
        return ReviewService(repository)