from app.ports.rest.api.v1.schema import BaseSchema


class PostImageAddSchema(BaseSchema):
    url: str
    order: int = 0


class PostImageResponseSchema(BaseSchema):
    id: int
    post_id: int
    url: str
    order: int