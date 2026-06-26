from app.adapters.database.tables import UserTable
from app.application.dto.user import UserResponseDTO, UserWithPasswordDTO


def converter_user(result: UserTable) -> UserResponseDTO:
    return UserResponseDTO(
        id=result.id,
        username=result.username,
        email=result.email,
        role=result.role,
        created_at=result.created_at,
        updated_at=result.updated_at,
        deleted_at=result.deleted_at,
    )


def converter_user_with_password(result: UserTable) -> UserWithPasswordDTO:
    return UserWithPasswordDTO(
        id=result.id,
        username=result.username,
        email=result.email,
        hashed_password=result.hashed_password,
        role=result.role,
        created_at=result.created_at,
        updated_at=result.updated_at,
        deleted_at=result.deleted_at,
    )
