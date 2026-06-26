from datetime import datetime

from app.ports.rest.api.v1.schema import BaseSchema


class PostCreateSchema(BaseSchema):
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    category_id: int | None = None


class PostUpdateSchema(BaseSchema):
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    category_id: int | None = None


class PostResponseSchema(BaseSchema):
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None
    price: float | None = None
    category_id: int | None = None
    created_by_id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ExistsParamsSchema(BaseSchema):
    id: int | None = None
