from dishka import Provider, Scope, provide

from app.adapters.database.repositories.users import UserRepository
from app.application.services.users import UserService


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_service(self, repository: UserRepository) -> UserService:
        return UserService(repository)