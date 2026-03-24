from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.adapters.database.mixins import IdMixin, TimestampSoftDeleteMixin


class Base(DeclarativeBase):
    pass


class User(Base, IdMixin, TimestampSoftDeleteMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
