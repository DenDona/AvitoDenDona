from typing import Annotated, Sequence

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.dto.user import UserResponseDTO
from app.application.services.auth_service import AuthService
from app.application.services.users import UserService
from app.ports.rest.api.v1.schemas.auth import UserResponse


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