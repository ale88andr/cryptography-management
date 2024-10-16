from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.connection import Base
from models.common import fields


class User(Base):
    __tablename__ = "user"

    id: Mapped[fields.pk]
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(50), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
