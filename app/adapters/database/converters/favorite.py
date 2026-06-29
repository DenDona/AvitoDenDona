from app.adapters.database.tables import FavoriteTable
from app.application.dto.favorite import FavoriteResponseDTO


def converter_favorite(result: FavoriteTable) -> FavoriteResponseDTO:
    return FavoriteResponseDTO(
        id=result.id,
        user_id=result.user_id,
        post_id=result.post_id,
        created_at=result.created_at,
    )
