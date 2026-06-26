from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.repositories.users import UserRepository
from app.application.services.auth_service import AuthService


class AuthProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def auth_service(self, repository: UserRepository) -> AuthService:
        return AuthService(repository)