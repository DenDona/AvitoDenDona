from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.repositories.chat import ChatRepository
from app.application.services.chat import ChatService


class ChatProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def chat_repository(self, session: AsyncSession) -> ChatRepository:
        return ChatRepository(session)

    @provide(scope=Scope.REQUEST)
    def chat_service(self, repository: ChatRepository) -> ChatService:
        return ChatService(repository)
