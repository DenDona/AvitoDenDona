from enum import Enum


class PostStatus(Enum):
    ACTIVE = "active"
    SOLD = "sold"
    ARCHIVED = "archived"
    MODERATION = "moderation"