import datetime
import enum
import orjson

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.connection import Base
from models.cryptography import Version, KeyDocument
from models.equipments import Equipment
from models.common import fields


ACTION_TYPES = [
    'Ввод СКЗИ в эксплуатацию',
    'Вывод СКЗИ из эксплуатации',
    'Установка',
    'Удаление',
    'Ввод кючевого документа из эксплуатации',
    'Вывод кючевого документа из эксплуатации',
]


class ActRecordTypes(enum.Enum):
    """Класс для описания типа события"""

    С_INSTALL = 0
    C_DESTRUCTION = 1
    I_INSTALL = 2
    I_REMOVE = "c_remove.docx"
    KD_INSTALL = 4
    KD_REMOVE = "kd_remove.docx"


class ActRecord(Base):
    __tablename__ = "cryptography_act_record"

    id: Mapped[fields.pk]
    action_type: Mapped[ActRecordTypes]
    number: Mapped[fields.title]
    reason: Mapped[str] = mapped_column(String(100), nullable=True)
    reason_date: Mapped[fields.date]
    action_date: Mapped[fields.required_date]
    head_commision_member_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=True
    )
    commision_member_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=True
    )
    performer_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=True
    )

    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

    install_object: Mapped["KeyDocument"] = relationship(
        uselist=False, foreign_keys=[KeyDocument.install_act_record_id]
    )

    remove_object: Mapped["KeyDocument"] = relationship(
        uselist=False, foreign_keys=[KeyDocument.remove_act_record_id]
    )

    head_commision_member: Mapped["Employee"] = relationship(
        uselist=False, foreign_keys=[head_commision_member_id]
    )

    commision_member: Mapped["Employee"] = relationship(
        uselist=False, foreign_keys=[commision_member_id]
    )

    performer: Mapped["Employee"] = relationship(
        uselist=False, foreign_keys=[performer_id]
    )

    def __str__(self) -> str:
        return f"Акт №{self.number}"

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


RECORD_TYPES = (
    "Установка СКЗИ, ввод в действие ключевого документа",
    "Удаление СКЗИ",
    "Обновление СКЗИ",
    "Ввод в действие ключевого документа",
    "Вывод ключевого документа из эксплуатации",
    "Компроментация ключей",
    "Техническое обслуживание СКЗИ",
    "Устранение технического сбоя",
)


class HardwareLogbookRecordType(enum.Enum):
    C_INSTALL = 0
    C_REMOVE = 1
    C_UPDATE = 2
    KD_INSTALL = 3
    KD_REMOVE = 4
    KD_DISCREDIT = 5
    C_MAINTANCE = 6
    C_FAILURE = 7


class HardwareLogbook(Base):
    __tablename__ = "cryptography_hardware_logbook"

    # Идентификатор записи журнала
    id: Mapped[fields.pk]

    # Идентификатор оборудования с которым ассоциируется запись журнала
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id", ondelete="CASCADE")
    )

    # Дата события записи журнала
    # *------*
    # | Дата |
    # *------*
    happened_at: Mapped[fields.required_date]

    # Версия СКЗИ установленная на оборудовании в момент события
    # *------------------------------------------*
    # | Тип и серийные номера используемых СКЗИ  |
    # *------------------------------------------*
    cryptography_version_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_version.id", ondelete="CASCADE"), nullable=False
    )

    # Тип события в соответствии с кортежем RECORD_TYPES
    # *-----------------------------*
    # | Записи по обслуживанию СКЗИ |
    # *-----------------------------*
    record_type: Mapped[HardwareLogbookRecordType]

    # Идентификатор ключевого документа введенного
    # в действие на момент записи журнала
    # *---------------------------*
    # | Используемые крипто ключи |
    # *---------------------------*
    key_document_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_key_document.id", ondelete="CASCADE"), nullable=True
    )

    # Актовая запись об удалении СКЗИ/Ключевых документов
    # *---------------------------------------------------------------*
    # | Отметка об уничтожении (стирании) - Подпись пользователя СКЗИ |
    # *---------------------------------------------------------------*
    remove_action_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id", ondelete="CASCADE"), nullable=True
    )

    # Дата удаления СКЗИ/Ключевых документов
    # *------------------------------------------*
    # | Отметка об уничтожении (стирании) - Дата |
    # *------------------------------------------*
    removed_at: Mapped[fields.date]

    # Примечание
    # *------------*
    # | Примечание |
    # *------------*
    comment: Mapped[str] = mapped_column(String(200), nullable=True)

    # Технические поля Создание/Обновление записей таблицы
    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

    cryptography_version: Mapped["Version"] = relationship()

    key_document: Mapped["KeyDocument"] = relationship()

    equipment: Mapped["Equipment"] = relationship(back_populates="hw_logs")

    remove_action: Mapped["ActRecord"] = relationship(
        uselist=False, foreign_keys=[remove_action_id]
    )

    def __str__(self) -> str:
        return f"{self.cryptography_version} ({self.happened_at})"

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class CryptographyPersonalAccount(Base):
    __tablename__ = "cryptography_personal_account"

    # Идентификатор записи журнала
    id: Mapped[fields.pk]

    # Идентификатор пользователя
    user_id: Mapped[int] = mapped_column(ForeignKey("employee.id", ondelete="CASCADE"))

    # Дата события записи журнала
    # *------*
    # | Дата |
    # *------*
    happened_at: Mapped[fields.required_date]

    # Версия СКЗИ установленная на оборудовании в момент события
    # *-------------------------------------------------------------------------------------------*
    # | Наименование СКЗИ, эксплуатационной и технической документации к ним, ключевых документов |
    # *-------------------------------------------------------------------------------------------*
    cryptography_version_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_version.id", ondelete="CASCADE"), nullable=False
    )

    # Идентификатор ключевого документа введенного
    # в действие на момент записи журнала
    # *---------------------------*
    # | Используемые крипто ключи |
    # *---------------------------*
    key_document_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_key_document.id", ondelete="CASCADE"), nullable=False
    )

    # Идентификатор оборудования с которым ассоциируется запись журнала
    # *---------------------------------------------------------------------------*
    # | Номера аппаратных средств, в которые установлены или к которым подключены |
    # *---------------------------------------------------------------------------*
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id", ondelete="CASCADE")
    )

    # Актовая запись об удалении СКЗИ/Ключевых документов
    # *--------------------------------------------------------*
    # | Номер и дата сопроводительного документа при получении |
    # *--------------------------------------------------------*
    install_action_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id", ondelete="CASCADE"), nullable=True
    )

    # Дата удаления СКЗИ/Ключевых документов
    # *------------------------------*
    # | Дата изъятия (деинсталляции) |
    # *------------------------------*
    removed_at: Mapped[fields.date]

    # Актовая запись об удалении СКЗИ/Ключевых документов
    # *---------------------------------------------------------------*
    # | Отметка об уничтожении (стирании) - Подпись пользователя СКЗИ |
    # *---------------------------------------------------------------*
    remove_action_id: Mapped[int] = mapped_column(
        ForeignKey("cryptography_act_record.id", ondelete="CASCADE"), nullable=True
    )

    # Примечание
    # *------------*
    # | Примечание |
    # *------------*
    comment: Mapped[str] = mapped_column(String(200), nullable=True)

    # Технические поля Создание/Обновление записей таблицы
    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

    cryptography_version: Mapped["Version"] = relationship(
        back_populates="personal_logs"
    )

    key_document: Mapped["KeyDocument"] = relationship()

    equipment: Mapped["Equipment"] = relationship()

    install_action: Mapped["ActRecord"] = relationship(
        uselist=False, foreign_keys=[install_action_id]
    )

    remove_action: Mapped["ActRecord"] = relationship(
        uselist=False, foreign_keys=[remove_action_id]
    )

    def __str__(self) -> str:
        return f"{self.cryptography_version} ({self.happened_at})"

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
