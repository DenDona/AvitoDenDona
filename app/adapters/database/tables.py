from sqlalchemy import String, Text, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.database.mixins import Base, IdMixin, TimestampSoftDeleteMixin
from app.application.enums.user_role import UserRole



class UserTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEES)


class PostTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    created_by_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
