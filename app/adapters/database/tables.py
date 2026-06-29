from sqlalchemy import String, Text, Numeric, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.database.mixins import Base, IdMixin, TimestampSoftDeleteMixin
from app.application.enums.post_condition import PostCondition
from app.application.enums.post_status import PostStatus
from app.application.enums.user_role import UserRole


class CategoryTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )


class UserTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEES)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)


class PostTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[PostStatus] = mapped_column(
        Enum(PostStatus), nullable=False, default=PostStatus.ACTIVE
    )
    condition: Mapped[PostCondition | None] = mapped_column(
        Enum(PostCondition), nullable=True
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )


class PostImageTable(Base, IdMixin):
    __tablename__ = "post_images"

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(String, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ConversationTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "conversations"

    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)


class MessageTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "messages"

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False
    )
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(nullable=False, default=False)


class FavoriteTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)


class ReviewTable(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "reviews"

    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[str | None] = mapped_column(Text, nullable=True)