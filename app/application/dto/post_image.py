from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class PostImageCreateDTO:
    post_id: int
    url: str
    order: int = 0


@dataclass(frozen=True, kw_only=True, slots=True)
class PostImageResponseDTO:
    id: int
    post_id: int
    url: str
    order: int