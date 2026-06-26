from collections.abc import Sequence
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.dto.user import UserResponseDTO
from app.application.services.auth_service import AuthService
from app.application.services.post_image import PostImageService
from app.ports.rest.api.v1.schemas.post_image import PostImageAddSchema, PostImageResponseSchema

post_image_router = APIRouter(prefix="/posts/{post_id}/images", tags=["post-images"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@post_image_router.get("/", response_model=Sequence[PostImageResponseSchema], status_code=status.HTTP_200_OK)
async def fetch_images(
        post_id: int,
        service: FromDishka[PostImageService],
) -> Sequence[PostImageResponseSchema]:
    images = await service.fetch_by_post(post_id=post_id)
    return [PostImageResponseSchema.model_validate(img) for img in images]


@post_image_router.post("/", response_model=PostImageResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_image(
        post_id: int,
        payload: PostImageAddSchema,
        service: FromDishka[PostImageService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> PostImageResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    image = await service.add(post_id=post_id, url=payload.url, order=payload.order, user=current_user)
    return PostImageResponseSchema.model_validate(image)


@post_image_router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
        post_id: int,
        image_id: int,
        service: FromDishka[PostImageService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> None:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    await service.delete(image_id=image_id, user=current_user)