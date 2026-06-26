from collections.abc import Sequence
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.dto.category import CategoryCreateDTO, CategoryUpdateDTO
from app.application.dto.user import UserResponseDTO
from app.application.services.auth_service import AuthService
from app.application.services.category import CategoryService
from app.ports.rest.api.v1.schemas.category import CategoryCreateSchema, CategoryUpdateSchema, CategoryResponseSchema

category_router = APIRouter(prefix="/categories", tags=["category"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@category_router.get("/", response_model=Sequence[CategoryResponseSchema], status_code=status.HTTP_200_OK)
async def fetch_list(
        service: FromDishka[CategoryService],
) -> Sequence[CategoryResponseSchema]:
    categories = await service.fetch_list()
    return [CategoryResponseSchema.model_validate(c) for c in categories]


@category_router.get("/{category_id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
async def fetch_by_id(
        category_id: int,
        service: FromDishka[CategoryService],
) -> CategoryResponseSchema:
    category = await service.fetch_by_id(category_id=category_id)
    return CategoryResponseSchema.model_validate(category)


@category_router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create(
        payload: CategoryCreateSchema,
        service: FromDishka[CategoryService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> CategoryResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    dto = CategoryCreateDTO(**payload.model_dump())
    category = await service.create(dto=dto, user=current_user)
    return CategoryResponseSchema.model_validate(category)


@category_router.patch("/{category_id}", response_model=CategoryResponseSchema, status_code=status.HTTP_200_OK)
async def update(
        category_id: int,
        payload: CategoryUpdateSchema,
        service: FromDishka[CategoryService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> CategoryResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    dto = CategoryUpdateDTO(**payload.model_dump(exclude_unset=True))
    category = await service.update_by_id(category_id=category_id, dto=dto, user=current_user)
    return CategoryResponseSchema.model_validate(category)


@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_soft(
        category_id: int,
        service: FromDishka[CategoryService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> None:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    await service.delete_soft(category_id=category_id, user=current_user)