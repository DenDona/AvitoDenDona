from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class ConversationCreateDTO:
    buyer_id: int
    seller_id: int
    post_id: int


@dataclass(frozen=True, kw_only=True, slots=True)
class ConversationResponseDTO:
    id: int
    buyer_id: int
    seller_id: int
    post_id: int
    created_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class MessageCreateDTO:
    conversation_id: int
    sender_id: int
    text: str


@dataclass(frozen=True, kw_only=True, slots=True)
class MessageResponseDTO:
    id: int
    conversation_id: int
    sender_id: int
    text: str
    is_read: bool
    created_at: datetime
