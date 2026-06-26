from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.repositories.favorite import FavoriteRepository
from app.application.services.favorite import FavoriteService


class FavoriteProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def favorite_repository(self, session: AsyncSession) -> FavoriteRepository:
        return FavoriteRepository(session)

    @provide(scope=Scope.REQUEST)
    def favorite_service(self, repository: FavoriteRepository) -> FavoriteService:
        return FavoriteService(repository)
