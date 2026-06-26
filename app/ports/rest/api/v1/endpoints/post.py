from collections.abc import Sequence
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.dto.post import PostCreateDTO, PostUpdateDTO
from app.application.dto.user import UserResponseDTO
from app.application.services.auth_service import AuthService
from app.application.services.post import PostService

from app.ports.rest.api.v1.schemas.post import PostResponseSchema, PostCreateSchema, PostUpdateSchema

post_router = APIRouter(prefix="/posts", tags=["post"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@post_router.post("/", response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED)
async def create(
        payload: PostCreateSchema,
        service: FromDishka[PostService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> PostResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    post_dto = PostCreateDTO(
        **payload.model_dump(),
        created_by_id=current_user.id,
    )
    post = await service.create(post_dto=post_dto)
    return PostResponseSchema.model_validate(post)


@post_router.patch("/{post_id}", response_model=PostResponseSchema, status_code=status.HTTP_200_OK)
async def update(
        post_id: int,
        payload: PostUpdateSchema,
        service: FromDishka[PostService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> PostResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    post_dto = PostUpdateDTO(**payload.model_dump(exclude_unset=True))
    post = await service.update_by_id(post_dto=post_dto, post_id=post_id, user=current_user)
    return PostResponseSchema.model_validate(post)


@post_router.get("/all/admin", response_model=Sequence[PostResponseSchema], status_code=status.HTTP_200_OK)
async def fetch_list(
        service: FromDishka[PostService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> Sequence[PostResponseSchema]:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    posts = await service.fetch_list(user=current_user)
    return [PostResponseSchema.model_validate(post) for post in posts]


@post_router.get("/", response_model=Sequence[PostResponseSchema], status_code=status.HTTP_200_OK)
async def fetch_list_as_user(
        service: FromDishka[PostService],
) -> Sequence[PostResponseSchema]:
    posts = await service.fetch_list_as_user()
    return [PostResponseSchema.model_validate(post) for post in posts]


@post_router.get("/{post_id}", response_model=PostResponseSchema, status_code=status.HTTP_200_OK)
async def fetch_by_id(
        post_id: int,
        service: FromDishka[PostService],
) -> PostResponseSchema:
    post = await service.fetch_by_id(post_id=post_id)
    return PostResponseSchema.model_validate(post)


@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_soft(
        post_id: int,
        service: FromDishka[PostService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
):
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    await service.delete_soft(post_id=post_id, user=current_user)
