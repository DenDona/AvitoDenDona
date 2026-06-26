from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.repositories.post_image import PostImageRepository
from app.application.services.post_image import PostImageService


class PostImageProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def post_image_repository(self, session: AsyncSession) -> PostImageRepository:
        return PostImageRepository(session)

    @provide(scope=Scope.REQUEST)
    def post_image_service(self, repository: PostImageRepository) -> PostImageService:
        return PostImageService(repository)