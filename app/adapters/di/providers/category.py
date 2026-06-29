from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.repositories.category import CategoryRepository
from app.application.services.category import CategoryService


class CategoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def category_repository(self, session: AsyncSession) -> CategoryRepository:
        return CategoryRepository(session)

    @provide(scope=Scope.REQUEST)
    def category_service(self, repository: CategoryRepository) -> CategoryService:
        return CategoryService(repository)