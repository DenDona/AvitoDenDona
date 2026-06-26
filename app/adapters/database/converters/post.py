from app.adapters.database.tables import PostTable
from app.application.dto.post import PostResponseDTO


def converter_post(result: PostTable) -> PostResponseDTO:
    return PostResponseDTO(
        id=result.id,
        title=result.title,
        description=result.description,
        image_url=result.image_url,
        price=result.price,
        created_by_id=result.created_by_id,
        created_at=result.created_at,
        updated_at=result.updated_at,
        deleted_at=result.deleted_at,
    )
