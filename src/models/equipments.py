import orjson

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.connection import Base
from models.common import fields


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[str] = mapped_column(String(25), primary_key=True)
    serial: Mapped[fields.title]
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    sticker: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)

    hw_logs: Mapped[list["HardwareLogbook"]] = relationship(back_populates="equipment")

    key_documents: Mapped[list["KeyDocument"]] = relationship(
        back_populates="equipment"
    )

    def __str__(self) -> str:
        return f"{self.id} ({self.sticker or '---'})"

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
