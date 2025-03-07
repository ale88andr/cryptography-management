import datetime
import orjson

from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.connection import Base
from models.common import fields


class Grade(Base):
    __tablename__ = "cryptography_grade"

    id: Mapped[fields.pk]
    value: Mapped[fields.title]
    description: Mapped[str] = mapped_column(Text(), nullable=True)

    def __str__(self) -> str:
        return self.value


class ProductType(Base):
    __tablename__ = "cryptography_product_type"

    id: Mapped[fields.pk]
    value: Mapped[fields.title]
    description: Mapped[str] = mapped_column(Text(), nullable=True)

    def __str__(self) -> str:
        return self.value


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


class Model(Base):
    __tablename__ = "cryptography_model"

    id: Mapped[fields.pk]
    name: Mapped[fields.title]
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    product_type_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_product_type.id")
    )
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_manufacturer.id")
    )

    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="models")
    product_type: Mapped["ProductType"] = relationship()
    versions: Mapped[list["Version"]] = relationship(back_populates="model")

    def __str__(self) -> str:
        return self.name

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class Version(Base):
    __tablename__ = "cryptography_version"

    id: Mapped[fields.pk]
    version: Mapped[str] = mapped_column(String(50), nullable=False)
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
        ForeignKey("cryptography_model.id")
    )
    responsible_user_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id")
    )
    install_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id")
    )
    remove_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id"), nullable=True
    )
    grade_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_grade.id"), nullable=True
    )
    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

    responsible_user: Mapped["Employee"] = relationship(
        back_populates="cryptography_set"
    )

    key_document_set: Mapped[list["KeyDocument"]] = relationship(
        back_populates="cryptography_version"
    )

    model: Mapped["Model"] = relationship(back_populates="versions")

    personal_logs: Mapped[list["CryptographyPersonalAccount"]] = relationship(
        back_populates="cryptography_version"
    )

    hw_logs: Mapped[list["HardwareLogbook"]] = relationship(
        back_populates="cryptography_version"
    )

    install_act: Mapped["ActRecord"] = relationship(
        uselist=False, foreign_keys=[install_act_record_id]
    )

    remove_act: Mapped["ActRecord"] = relationship(
        uselist=False, foreign_keys=[remove_act_record_id]
    )

    grade_class: Mapped["Grade"] = relationship()

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
    carrier_type_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_key_carrier_type.id")
    )

    carrier_type: Mapped["KeyCarrierType"] = relationship(back_populates="carriers")

    key_documents: Mapped[list["KeyDocument"]] = relationship(
        back_populates="key_carrier"
    )

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
        ForeignKey("cryptography_version.id")
    )
    carrier_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_key_carrier.id")
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id")
    )
    install_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id"),
    )
    remove_act_record_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id"), nullable=True
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
    )

    remove_act: Mapped["ActRecord"] = relationship(
        back_populates="remove_object",
        uselist=False,
        foreign_keys=[remove_act_record_id],
    )

    def __str__(self) -> str:
        return f"{self.serial} ({self.key_carrier})"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps
