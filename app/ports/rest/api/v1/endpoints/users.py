from typing import Annotated, Sequence

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.dto.user import UserResponseDTO, UserUpdateDTO
from app.application.services.auth_service import AuthService
from app.application.services.users import UserService
from app.ports.rest.api.v1.schemas.auth import UserResponse, UserUpdateRequest


user_router = APIRouter(prefix="/users", tags=["user"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@user_router.get("/", response_model=Sequence[UserResponse], status_code=status.HTTP_200_OK)
async def fetch_users(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    auth_service: FromDishka[AuthService],
    service: FromDishka[UserService],
) -> Sequence[UserResponse]:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    users = await service.fetch_users(user=current_user)
    return [UserResponse.model_validate(u) for u in users]


@user_router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    payload: UserUpdateRequest,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    auth_service: FromDishka[AuthService],
    service: FromDishka[UserService],
) -> UserResponse:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    dto = UserUpdateDTO(**payload.model_dump(exclude_unset=True))
    user = await service.update_profile(user_id=current_user.id, dto=dto)
    return UserResponse.model_validate(user)


@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    service: FromDishka[UserService],
) -> UserResponse:
    user = await service.get_by_id(user_id)
    return UserResponse.model_validate(user)