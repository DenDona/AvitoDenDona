from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.session import SessionLocal


class SessionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncIterable[AsyncSession]:
        async with SessionLocal() as session:
            yield session