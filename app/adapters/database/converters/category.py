from app.adapters.database.tables import CategoryTable
from app.application.dto.category import CategoryResponseDTO


def converter_category(result: CategoryTable) -> CategoryResponseDTO:
    return CategoryResponseDTO(
        id=result.id,
        name=result.name,
        parent_id=result.parent_id,
        created_at=result.created_at,
        updated_at=result.updated_at,
        deleted_at=result.deleted_at,
    )