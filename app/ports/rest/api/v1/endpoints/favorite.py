from collections.abc import Sequence
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.dto.user import UserResponseDTO
from app.application.services.auth_service import AuthService
from app.application.services.favorite import FavoriteService
from app.ports.rest.api.v1.schemas.favorite import FavoriteResponseSchema

favorite_router = APIRouter(prefix="/favorites", tags=["favorites"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@favorite_router.get("/", response_model=Sequence[FavoriteResponseSchema], status_code=status.HTTP_200_OK)
async def fetch_favorites(
        service: FromDishka[FavoriteService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> Sequence[FavoriteResponseSchema]:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    favorites = await service.fetch_by_user(user_id=current_user.id)
    return [FavoriteResponseSchema.model_validate(f) for f in favorites]


@favorite_router.post("/{post_id}", response_model=FavoriteResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_favorite(
        post_id: int,
        service: FromDishka[FavoriteService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> FavoriteResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    favorite = await service.add(user_id=current_user.id, post_id=post_id)
    return FavoriteResponseSchema.model_validate(favorite)


@favorite_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
        post_id: int,
        service: FromDishka[FavoriteService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> None:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    await service.remove(user_id=current_user.id, post_id=post_id)
