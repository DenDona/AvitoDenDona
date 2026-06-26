from collections.abc import Sequence

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.converters.chat import converter_conversation, converter_message
from app.adapters.database.tables import ConversationTable, MessageTable
from app.application.dto.chat import (
    ConversationCreateDTO, ConversationResponseDTO,
    MessageCreateDTO, MessageResponseDTO,
)


class ChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_or_create_conversation(self, dto: ConversationCreateDTO) -> ConversationResponseDTO:
        stmt = select(ConversationTable).where(
            ConversationTable.buyer_id == dto.buyer_id,
            ConversationTable.seller_id == dto.seller_id,
            ConversationTable.post_id == dto.post_id,
            ConversationTable.deleted_at.is_(None),
        )
        existing = await self.__session.scalar(stmt)
        if existing:
            return converter_conversation(existing)

        insert_stmt = (
            insert(ConversationTable).values(
                buyer_id=dto.buyer_id,
                seller_id=dto.seller_id,
                post_id=dto.post_id,
            )
        ).returning(ConversationTable)
        result = (await self.__session.scalars(insert_stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_conversation(result)

    async def fetch_conversations_for_user(self, user_id: int) -> Sequence[ConversationResponseDTO]:
        stmt = (
            select(ConversationTable)
            .where(
                (ConversationTable.buyer_id == user_id) | (ConversationTable.seller_id == user_id),
                ConversationTable.deleted_at.is_(None),
            )
            .order_by(ConversationTable.created_at.desc())
        )
        result = await self.__session.execute(stmt)
        return [converter_conversation(row) for row in result.scalars().all()]

    async def create_message(self, dto: MessageCreateDTO) -> MessageResponseDTO:
        stmt = (
            insert(MessageTable).values(
                conversation_id=dto.conversation_id,
                sender_id=dto.sender_id,
                text=dto.text,
            )
        ).returning(MessageTable)
        result = (await self.__session.scalars(stmt)).one()
        await self.__session.commit()
        await self.__session.refresh(result)
        return converter_message(result)

    async def fetch_messages(self, conversation_id: int) -> Sequence[MessageResponseDTO]:
        stmt = (
            select(MessageTable)
            .where(MessageTable.conversation_id == conversation_id)
            .order_by(MessageTable.created_at)
        )
        result = await self.__session.execute(stmt)
        return [converter_message(row) for row in result.scalars().all()]

    async def mark_read(self, conversation_id: int, user_id: int) -> None:
        stmt = (
            update(MessageTable)
            .where(
                MessageTable.conversation_id == conversation_id,
                MessageTable.sender_id != user_id,
                MessageTable.is_read == False,
            )
            .values(is_read=True)
        )
        await self.__session.execute(stmt)
        await self.__session.commit()
