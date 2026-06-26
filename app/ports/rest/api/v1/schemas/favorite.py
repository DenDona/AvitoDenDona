from datetime import datetime

from app.ports.rest.api.v1.schema import BaseSchema


class FavoriteResponseSchema(BaseSchema):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
