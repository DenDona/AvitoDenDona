from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.repositories.post import PostRepository
from app.application.services.post import PostService


class PostProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def post_repository(self, session: AsyncSession) -> PostRepository:
        return PostRepository(session)

    @provide(scope=Scope.REQUEST)
    def post_service(self, repository: PostRepository) -> PostService:
        return PostService(repository)