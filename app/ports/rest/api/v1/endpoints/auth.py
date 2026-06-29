from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.services.auth_service import AuthService
from app.ports.rest.api.v1.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


auth_router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    service: FromDishka[AuthService],
) -> UserResponse:
    user = await service.register(username=payload.username, email=payload.email, password=payload.password)
    return UserResponse.model_validate(user)


@auth_router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginRequest,
    service: FromDishka[AuthService],
) -> TokenResponse:
    access_token = await service.login(login=payload.login, password=payload.password)
    return TokenResponse(access_token=access_token)


@auth_router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    service: FromDishka[AuthService],
) -> UserResponse:
    user = await service.get_user_from_token(credentials.credentials)
    return UserResponse.model_validate(user)
