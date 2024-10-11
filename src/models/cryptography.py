import datetime
import enum
import orjson

from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.connection import Base
from models.common import fields


class Manufacturer(Base):
    __tablename__ = "cryptography_manufacturer"

    id: Mapped[fields.pk]
    name: Mapped[fields.title]

    models: Mapped[list["Model"]] = relationship(back_populates="manufacturer")

    def __str__(self):
        return self.name

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


CRYPTO_MODEL_TYPES = [
    'Программный',
    'Аппаратный',
    'Аппаратно-программный'
]


class ModelTypes(enum.Enum):
    """Enum типов СКЗИ"""
    PROGRAM  = 0
    HARDWARE = 1
    HARDSOFT = 2


class Model(Base):
    __tablename__ = "cryptography_model"

    id: Mapped[fields.pk]
    name: Mapped[fields.title]
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    type: Mapped[ModelTypes] = mapped_column(default=ModelTypes.PROGRAM)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("cryptography_manufacturer.id", ondelete="CASCADE"))

    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="models")
    versions: Mapped[list["Version"]] = relationship(back_populates="model")

    def __str__(self) -> str:
        return self.name

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


CPRODUCT_GRADES = [
    "КС1",
    "КС2",
    "КС3",
    "КВ1",
    "КВ2",
    "КА1"
]


class CryptographyGrade(enum.Enum):
    """Enum исполнений СКЗИ"""

    KC1 = 0
    KC2 = 1
    KC3 = 2
    KB1 = 3
    KB2 = 4
    KA1 = 5


class Version(Base):
    __tablename__ = "cryptography_version"

    id: Mapped[fields.pk]
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    grade: Mapped[CryptographyGrade]
    serial: Mapped[str] = mapped_column(String(50), nullable=False)
    dist_num: Mapped[str] = mapped_column(String(50), nullable=False)
    certificate: Mapped[str] = mapped_column(String(20), nullable=False)
    certificate_expired_at: Mapped[fields.date]
    received_from: Mapped[str] = mapped_column(String(50), nullable=False)
    received_num: Mapped[str] = mapped_column(String(50), nullable=False)
    received_at: Mapped[fields.required_date]
    form: Mapped[str] = mapped_column(String(50), nullable=False)
    license: Mapped[str] = mapped_column(String(150), nullable=True)
    comment: Mapped[str] = mapped_column(String(200), nullable=True)
    model_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_model.id", ondelete="CASCADE")
    )
    responsible_user_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE")
    )
    install_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id", ondelete="CASCADE")
    )
    remove_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id", ondelete="CASCADE"),
        nullable=True
    )
    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

    responsible_user: Mapped["Employee"] = relationship(
        back_populates="cryptography_set"
    )

    key_document_set: Mapped[list["KeyDocument"]] = relationship(
        back_populates="cryptography_version"
    )

    model: Mapped["Model"] = relationship(
        back_populates="versions"
    )

    personal_logs: Mapped[list["CryptographyPersonalAccount"]] = relationship(
        back_populates="cryptography_version"
    )

    hw_logs: Mapped[list["HardwareLogbook"]] = relationship(
        back_populates="cryptography_version"
    )

    install_act: Mapped["ActRecord"] = relationship(
        uselist=False,
        foreign_keys=[install_act_record_id]
    )

    remove_act: Mapped["ActRecord"] = relationship(
        uselist=False,
        foreign_keys=[remove_act_record_id]
    )

    def is_certificate_expired(self):
        if self.certificate_expired_at:
            return self.certificate_expired_at < datetime.date.today()

        return True

    @property
    def doc_set(self):
        cryptography = f"СКЗИ {self.title} сер. номер {self.serial}"
        dist = f"Дистрибутив, учетный номер {self.dist_num}" if self.dist_num else None
        form = f"Формуляр {self.form}"
        license = f"Лицензия: {self.license}" if self.license else None
        return [item for item in [cryptography, dist, form, license] if item]

    @property
    def received_doc(self):
        return f"№ {self.received_num} от {self.received_at.strftime('%d.%m.%Y')}"

    @property
    def title(self):
        return f"{self.model} (версия {self.version})"

    @property
    def cert_info(self):
        return f"{self.certificate or '---'} ({self.certificate_expired_at.strftime('%d.%m.%Y') if self.certificate_expired_at else '---'})"

    @property
    def serial_nums(self):
        s_dist = f"; № дист: {self.dist_num}" if self.dist_num else ""
        return f"СКЗИ: {self.serial}{s_dist}"

    def __str__(self) -> str:
        return f"{self.model.name} {self.version} (№ дистр. {self.dist_num or '---'}, СКЗИ {self.serial})"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class KeyCarrierType(Base):
    __tablename__ = "cryptography_key_carrier_type"

    id: Mapped[fields.pk]
    name: Mapped[fields.title]

    carriers: Mapped[list["KeyCarrier"]] = relationship(back_populates="carrier_type")

    def __str__(self):
        return self.name

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class KeyCarrier(Base):
    __tablename__ = "cryptography_key_carrier"

    id: Mapped[fields.pk]
    serial: Mapped[fields.title]
    carrier_type_id: Mapped[int] = mapped_column(ForeignKey("cryptography_key_carrier_type.id", ondelete="CASCADE"))

    carrier_type: Mapped["KeyCarrierType"] = relationship(back_populates="carriers")
    key_documents: Mapped[list["KeyDocument"]] = relationship(back_populates="key_carrier")

    def __str__(self) -> str:
        return f"{self.serial} ({self.carrier_type})"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class KeyDocument(Base):
    __tablename__ = "cryptography_key_document"

    id: Mapped[fields.pk]
    serial: Mapped[fields.title]
    is_unexpired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    received_from: Mapped[str] = mapped_column(String(50), nullable=False)
    received_date: Mapped[fields.required_date]
    comment: Mapped[str] = mapped_column(String(200), nullable=True)
    cryptography_version_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_version.id", ondelete="CASCADE")
    )
    carrier_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_key_carrier.id", ondelete="CASCADE")
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE")
    )
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id", ondelete="CASCADE")
    )
    install_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id", ondelete="CASCADE"),
    )
    remove_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id", ondelete="CASCADE"),
        nullable=True
    )
    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

    cryptography_version: Mapped["Version"] = relationship(
        back_populates="key_document_set",
    )

    key_carrier: Mapped["KeyCarrier"] = relationship(
        back_populates="key_documents",
    )

    owner: Mapped["Employee"] = relationship(
        back_populates="key_document_set",
    )

    equipment: Mapped["Equipment"] = relationship(
        back_populates="key_documents",
    )

    install_act: Mapped["ActRecord"] = relationship(
        back_populates="install_object",
        uselist=False,
        foreign_keys=[install_act_record_id],
        order_by="desc(ActRecord.action_date)"
    )

    remove_act: Mapped["ActRecord"] = relationship(
        back_populates="remove_object",
        uselist=False,
        foreign_keys=[remove_act_record_id]
    )

    def __str__(self) -> str:
        return f"{self.serial} ({self.key_carrier})"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps
