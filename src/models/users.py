from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.connection import Base
from models.common import fields


class User(Base):
    __tablename__ = "user"
    # One to One relation
    __table_args__ = (UniqueConstraint("employee_id"),)

    id: Mapped[fields.pk]
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_password_temporary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_login_at: Mapped[fields.dtime]
    last_login_from: Mapped[str] = mapped_column(String(250), nullable=True)
    last_login_ip: Mapped[str] = mapped_column(String(50), nullable=True)
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=True
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="user", lazy="joined"
    )

    def __str__(self) -> str:
        return self.email.split('@')[0]
