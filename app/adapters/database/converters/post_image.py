from app.adapters.database.tables import PostImageTable
from app.application.dto.post_image import PostImageResponseDTO


def converter_post_image(result: PostImageTable) -> PostImageResponseDTO:
    return PostImageResponseDTO(
        id=result.id,
        post_id=result.post_id,
        url=result.url,
        order=result.order,
    )