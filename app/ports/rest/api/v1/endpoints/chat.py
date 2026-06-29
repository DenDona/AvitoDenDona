import json
from collections.abc import Sequence
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.adapters.redis import redis_client
from app.application.dto.user import UserResponseDTO
from app.application.services.auth_service import AuthService
from app.application.services.chat import ChatService
from app.ports.rest.api.v1.schemas.chat import (
    ConversationCreateSchema, ConversationResponseSchema,
    MessageSendSchema, MessageResponseSchema,
)

chat_router = APIRouter(prefix="/chat", tags=["chat"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@chat_router.post("/conversations", response_model=ConversationResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_conversation(
        payload: ConversationCreateSchema,
        service: FromDishka[ChatService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> ConversationResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    conversation = await service.get_or_create_conversation(
        buyer_id=current_user.id,
        seller_id=payload.seller_id,
        post_id=payload.post_id,
    )
    return ConversationResponseSchema.model_validate(conversation)


@chat_router.get("/conversations", response_model=Sequence[ConversationResponseSchema], status_code=status.HTTP_200_OK)
async def fetch_conversations(
        service: FromDishka[ChatService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> Sequence[ConversationResponseSchema]:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    conversations = await service.fetch_my_conversations(user=current_user)
    return [ConversationResponseSchema.model_validate(c) for c in conversations]


@chat_router.get("/conversations/{conversation_id}/messages", response_model=Sequence[MessageResponseSchema])
async def fetch_messages(
        conversation_id: int,
        service: FromDishka[ChatService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> Sequence[MessageResponseSchema]:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    await service.mark_read(conversation_id=conversation_id, user=current_user)
    messages = await service.fetch_messages(conversation_id=conversation_id, user=current_user)
    return [MessageResponseSchema.model_validate(m) for m in messages]


@chat_router.post("/conversations/{conversation_id}/messages", response_model=MessageResponseSchema, status_code=status.HTTP_201_CREATED)
async def send_message(
        conversation_id: int,
        payload: MessageSendSchema,
        service: FromDishka[ChatService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> MessageResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    message = await service.send_message(
        conversation_id=conversation_id, text=payload.text, user=current_user
    )
    await redis_client.publish(
        f"chat:{conversation_id}",
        json.dumps({"id": message.id, "sender_id": message.sender_id, "text": message.text}),
    )
    return MessageResponseSchema.model_validate(message)


@chat_router.websocket("/ws/{conversation_id}")
async def websocket_chat(
        websocket: WebSocket,
        conversation_id: int,
        token: str = Query(...),
) -> None:
    from dishka import AsyncContainer
    container: AsyncContainer = websocket.app.state.dishka_container
    async with container() as request_container:
        auth_service = await request_container.get(AuthService)
        try:
            await auth_service.get_user_from_token(token)
        except Exception:
            await websocket.close(code=1008)
            return

    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"chat:{conversation_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(f"chat:{conversation_id}")
        await pubsub.aclose()
