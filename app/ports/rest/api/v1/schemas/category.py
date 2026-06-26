from datetime import datetime

from app.ports.rest.api.v1.schema import BaseSchema


class CategoryCreateSchema(BaseSchema):
    name: str
    parent_id: int | None = None


class CategoryUpdateSchema(BaseSchema):
    name: str | None = None
    parent_id: int | None = None


class CategoryResponseSchema(BaseSchema):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime
