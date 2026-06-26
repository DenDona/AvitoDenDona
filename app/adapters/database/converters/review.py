from app.adapters.database.tables import ReviewTable
from app.application.dto.review import ReviewResponseDTO


def converter_review(result: ReviewTable) -> ReviewResponseDTO:
    return ReviewResponseDTO(
        id=result.id,
        from_user_id=result.from_user_id,
        to_user_id=result.to_user_id,
        rating=result.rating,
        text=result.text,
        created_at=result.created_at,
    )