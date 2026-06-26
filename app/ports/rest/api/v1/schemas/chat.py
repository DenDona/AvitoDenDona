from datetime import datetime

from app.ports.rest.api.v1.schema import BaseSchema


class ConversationCreateSchema(BaseSchema):
    seller_id: int
    post_id: int


class ConversationResponseSchema(BaseSchema):
    id: int
    buyer_id: int
    seller_id: int
    post_id: int
    created_at: datetime


class MessageSendSchema(BaseSchema):
    text: str


class MessageResponseSchema(BaseSchema):
    id: int
    conversation_id: int
    sender_id: int
    text: str
    is_read: bool
    created_at: datetime
