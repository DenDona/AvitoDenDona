from datetime import datetime

from app.application.enums.post_condition import PostCondition
from app.application.enums.post_status import PostStatus
from app.ports.rest.api.v1.schema import BaseSchema


class PostCreateSchema(BaseSchema):
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    city: str | None = None
    condition: PostCondition | None = None
    category_id: int | None = None


class PostUpdateSchema(BaseSchema):
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    city: str | None = None
    status: PostStatus | None = None
    condition: PostCondition | None = None
    category_id: int | None = None


class PostResponseSchema(BaseSchema):
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    city: str | None = None
    status: PostStatus = PostStatus.ACTIVE
    condition: PostCondition | None = None
    category_id: int | None = None
    created_by_id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class PaginatedPostResponseSchema(BaseSchema):
    items: list[PostResponseSchema]
    total: int
    page: int
    limit: int


class ExistsParamsSchema(BaseSchema):
    id: int | None = None