from collections.abc import Sequence
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.application.dto.user import UserResponseDTO
from app.application.services.auth_service import AuthService
from app.application.services.review import ReviewService
from app.ports.rest.api.v1.schemas.review import ReviewCreateSchema, ReviewResponseSchema, UserRatingSummarySchema

review_router = APIRouter(prefix="/reviews", tags=["reviews"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()


@review_router.get("/users/{user_id}", response_model=Sequence[ReviewResponseSchema], status_code=status.HTTP_200_OK)
async def fetch_reviews_for_user(
        user_id: int,
        service: FromDishka[ReviewService],
) -> Sequence[ReviewResponseSchema]:
    reviews = await service.fetch_for_user(to_user_id=user_id)
    return [ReviewResponseSchema.model_validate(r) for r in reviews]


@review_router.get("/users/{user_id}/rating", response_model=UserRatingSummarySchema, status_code=status.HTTP_200_OK)
async def get_user_rating(
        user_id: int,
        service: FromDishka[ReviewService],
) -> UserRatingSummarySchema:
    summary = await service.get_rating_summary(to_user_id=user_id)
    return UserRatingSummarySchema.model_validate(summary)


@review_router.post("/users/{user_id}", response_model=ReviewResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
        user_id: int,
        payload: ReviewCreateSchema,
        service: FromDishka[ReviewService],
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> ReviewResponseSchema:
    current_user: UserResponseDTO = await auth_service.get_user_from_token(credentials.credentials)
    review = await service.create(
        to_user_id=user_id,
        rating=payload.rating,
        text=payload.text,
        user=current_user,
    )
    return ReviewResponseSchema.model_validate(review)