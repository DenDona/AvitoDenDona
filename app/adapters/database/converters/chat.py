from app.adapters.database.tables import ConversationTable, MessageTable
from app.application.dto.chat import ConversationResponseDTO, MessageResponseDTO


def converter_conversation(result: ConversationTable) -> ConversationResponseDTO:
    return ConversationResponseDTO(
        id=result.id,
        buyer_id=result.buyer_id,
        seller_id=result.seller_id,
        post_id=result.post_id,
        created_at=result.created_at,
    )


def converter_message(result: MessageTable) -> MessageResponseDTO:
    return MessageResponseDTO(
        id=result.id,
        conversation_id=result.conversation_id,
        sender_id=result.sender_id,
        text=result.text,
        is_read=result.is_read,
        created_at=result.created_at,
    )
