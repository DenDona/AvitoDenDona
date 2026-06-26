from collections.abc import Sequence

from app.adapters.database.repositories.chat import ChatRepository
from app.application.dto.chat import (
    ConversationCreateDTO, ConversationResponseDTO,
    MessageCreateDTO, MessageResponseDTO,
)
from app.application.dto.user import UserResponseDTO
from app.cammon.exceptions import PermissionDeniedException


class ChatService:
    def __init__(self, repository: ChatRepository) -> None:
        self._repository = repository

    async def get_or_create_conversation(
        self, buyer_id: int, seller_id: int, post_id: int
    ) -> ConversationResponseDTO:
        dto = ConversationCreateDTO(buyer_id=buyer_id, seller_id=seller_id, post_id=post_id)
        return await self._repository.get_or_create_conversation(dto=dto)

    async def fetch_my_conversations(self, user: UserResponseDTO) -> Sequence[ConversationResponseDTO]:
        return await self._repository.fetch_conversations_for_user(user_id=user.id)

    async def send_message(
        self, conversation_id: int, text: str, user: UserResponseDTO
    ) -> MessageResponseDTO:
        dto = MessageCreateDTO(conversation_id=conversation_id, sender_id=user.id, text=text)
        return await self._repository.create_message(dto=dto)

    async def fetch_messages(
        self, conversation_id: int, user: UserResponseDTO
    ) -> Sequence[MessageResponseDTO]:
        return await self._repository.fetch_messages(conversation_id=conversation_id)

    async def mark_read(self, conversation_id: int, user: UserResponseDTO) -> None:
        await self._repository.mark_read(conversation_id=conversation_id, user_id=user.id)
