import math
from datetime import date, datetime
from typing import Optional
from sqlalchemy import select, update, text, func, extract
from sqlalchemy.orm import joinedload

from db.connection import db
from models.logbook import (
    ActRecord,
    ActRecordTypes,
    CryptographyPersonalAccount,
    HardwareLogbook,
    HardwareLogbookRecordType,
)
from admin.constants import ADMIN_CILOG_CHANGE_REASONS as replace_reasons
from models.staff import Employee
from services.base import BaseRepository
from models.cryptography import KeyCarrier, KeyDocument, Model, Version
from services.c_action import CActionServise
from services.c_hardware_logbook import CHardwareLogbookServise
from services.employee_personal_account import EmployeePersonalAccountService
from utils.formatting import format_date


class KeyDocumentServise(BaseRepository):
    model = KeyDocument

    @classmethod
    async def get_list(cls, sort: str = None, q: str = None, filters: Optional[dict] = None):
        query = select(cls.model).options(
            joinedload(cls.model.key_carrier).options(
                joinedload(KeyCarrier.carrier_type)
            )
        )

        # Filter rows
        if filters:
            query = query.filter_by(**filters)

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.serial.ilike(f"%{text(q)}%"))

        records = (await db.execute(query)).scalars().all()

        return records, len(records)

    @classmethod
    async def latest(cls, limit: int = 10):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.cryptography_version).options(
                    joinedload(Version.model)
                ),
                joinedload(cls.model.install_act).options(
                    joinedload(ActRecord.performer)
                ),
                joinedload(cls.model.owner).options(
                    joinedload(Employee.department)
                ),
                joinedload(cls.model.key_carrier).options(
                    joinedload(KeyCarrier.carrier_type)
                ),
            )
            .limit(limit)
        )
        records = (await db.execute(query)).scalars().all()
        return records

    @classmethod
    async def all_with_pagination(
        cls,
        page: int = 0,
        limit: int = 0,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None,
    ):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.cryptography_version).options(
                    joinedload(Version.model)
                ),
                joinedload(cls.model.key_carrier).options(
                    joinedload(KeyCarrier.carrier_type)
                ),
                joinedload(cls.model.equipment),
                joinedload(cls.model.owner),
                joinedload(cls.model.install_act).options(
                    joinedload(ActRecord.performer)
                ),
                joinedload(cls.model.remove_act).options(
                    joinedload(ActRecord.performer)
                ),
            )
            .join(ActRecord, cls.model.install_act)
        )

        if filters.get("is_active"):
            query = query.filter(cls.model.remove_act_record_id.is_(None))

        if filters.get("is_disable"):
            query = query.filter(cls.model.remove_act_record_id.is_not(None))

        if filters.get("is_unexpired"):
            query = query.filter(cls.model.is_unexpired.is_(True))

        if filters.get("is_expired"):
            query = query.filter(cls.model.is_unexpired.is_(False))

        if filters.get("owner_id"):
            query = query.filter(cls.model.owner_id==filters["owner_id"])

        if filters.get("carrier_id"):
            query = query.filter(cls.model.carrier_id==filters["carrier_id"])

        if filters.get("version_id"):
            query = query.filter(cls.model.cryptography_version_id==filters["version_id"])

        if filters.get("performer_id"):
            query = query.filter(ActRecord.performer_id==filters["performer_id"])

        if filters.get("date_from"):
            query = query.filter(func.date(ActRecord.action_date)>=filters["date_from"])

        if filters.get("date_to"):
            query = query.filter(func.date(ActRecord.action_date)<=filters["date_to"])

        if not sort and sort != "null":
            query = query.order_by(
                ActRecord.action_date.desc(),
                cls.model.install_act_record_id.desc()
            )
        else:
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.serial.ilike(f"%{text(q)}%"))

        if limit:
            query = query.offset(page * limit).limit(limit)

        count_query = select(func.count(1)).select_from(cls.model)

        total_records = (await db.execute(count_query)).scalar() or 0
        total_pages = math.ceil(total_records / limit) if limit else 0

        records = (await db.execute(query)).scalars().all()

        return records, len(records), total_records, total_pages

    @classmethod
    async def all_expired(cls):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.cryptography_version),
                joinedload(cls.model.cryptography_version).options(
                    joinedload(Version.model)
                ),
                joinedload(cls.model.key_carrier).options(
                    joinedload(KeyCarrier.carrier_type)
                ),
                joinedload(cls.model.owner)
            )
            .filter_by(is_unexpired=False, remove_act_record_id=None)
        )
        result = await cls.db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.equipment),
                joinedload(cls.model.cryptography_version),
                joinedload(cls.model.cryptography_version).options(
                    joinedload(Version.model).options(joinedload(Model.product_type)),
                    joinedload(Version.grade_class)
                ),
                joinedload(cls.model.key_carrier).options(
                    joinedload(KeyCarrier.carrier_type)
                ),
                joinedload(cls.model.owner).options(
                    joinedload(Employee.position),
                    joinedload(Employee.department),
                    joinedload(Employee.location),
                    joinedload(Employee.organisation),
                ),
                joinedload(cls.model.install_act).options(
                    joinedload(ActRecord.performer).options(
                        joinedload(Employee.position), joinedload(Employee.department)
                    ),
                    joinedload(ActRecord.head_commision_member).options(
                        joinedload(Employee.position), joinedload(Employee.department)
                    ),
                    joinedload(ActRecord.commision_member).options(
                        joinedload(Employee.position), joinedload(Employee.department)
                    ),
                ),
                joinedload(cls.model.remove_act).options(
                    joinedload(ActRecord.performer).options(
                        joinedload(Employee.position), joinedload(Employee.department)
                    ),
                    joinedload(ActRecord.head_commision_member).options(
                        joinedload(Employee.position), joinedload(Employee.department)
                    ),
                    joinedload(ActRecord.commision_member).options(
                        joinedload(Employee.position), joinedload(Employee.department)
                    ),
                ),
            )
            .filter_by(id=int(model_id))
        )
        result = await cls.db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def destruct_key(
        cls, key_document: KeyDocument, act_record: ActRecord, action_date: date
    ):
        try:
            await cls.remove_key(
                log_id=key_document.log.id,
                key_id=key_document.id,
                act_record_id=act_record.id,
                action_date=action_date,
            )
            await cls.db.commit()
            await cls.db.refresh(key_document)
            await cls.db.session.flush()
        except Exception as e:
            print(f"--------- Exception in {cls.__name__}.destruct_key() ---------")
            print(e)
            print(f"--------- Exception in {cls.__name__}.destruct_key() ---------")
            await cls.db.rollback()

    @classmethod
    async def destruct_c_version(
        cls, keys: list[KeyDocument], act_record: ActRecord, action_date: date
    ):
        try:
            for key in keys:
                await cls.remove_key(
                    key_id=key.id, act_record_id=act_record.id, action_date=action_date
                )

            await cls.db.commit()
            await cls.db.session.flush()
        except Exception as e:
            print(
                f"--------- Exception in {cls.__name__}.destruct_c_version() ---------"
            )
            print(e)
            print(
                f"--------- Exception in {cls.__name__}.destruct_c_version() ---------"
            )
            await cls.db.rollback()

    @classmethod
    async def remove_key(cls, key_id: int, act_record_id: int, action_date: date):
        # Обновление записи журнала поэкземплярного учета
        await cls.db.execute(
            update(KeyDocument)
            .where(KeyDocument.id == key_id)
            .values(remove_act_record_id=act_record_id)
        )

        # Обновление записи аппаратного журнала
        await cls.db.execute(
            update(HardwareLogbook)
            .where(HardwareLogbook.key_document_id == key_id)
            .values(remove_action_id=act_record_id, removed_at=action_date)
        )

        # Обновление записи в лицевом счете сотрудника
        await cls.db.execute(
            update(CryptographyPersonalAccount)
            .where(CryptographyPersonalAccount.key_document_id == key_id)
            .values(remove_action_id=act_record_id, removed_at=action_date)
        )

    @classmethod
    async def add_unexpired_key(cls, **key_data):
        return await cls.__add_key(**key_data, is_unexpired=True)

    @classmethod
    async def add_expired_key(cls, **key_data):
        return await cls.__add_key(**key_data)

    @classmethod
    async def __add_key(
        cls,
        serial: str,
        cryptography_version_id: int,
        carrier_id: int,
        owner_id: int,
        equipment_id: int,
        received_from: str,
        received_date: date,
        install_act_record: ActRecord,
        comment: str | None = None,
        is_unexpired: bool = False,
    ):
        key_document = await cls.add(
            serial=serial,
            cryptography_version_id=cryptography_version_id,
            carrier_id=carrier_id,
            owner_id=owner_id,
            equipment_id=equipment_id,
            received_from=received_from,
            received_date=received_date,
            install_act_record_id=install_act_record.id,
            comment=comment,
            is_unexpired=is_unexpired,
        )

        # Создание записи аппаратного журнала
        await CHardwareLogbookServise.add(
            record_type=HardwareLogbookRecordType.KD_INSTALL,
            equipment_id=equipment_id,
            happened_at=install_act_record.action_date,
            key_document_id=key_document.id,
            cryptography_version_id=cryptography_version_id,
        )

        # Создание записи Лицевого счета
        await EmployeePersonalAccountService.add(
            equipment_id=equipment_id,
            user_id=owner_id,
            happened_at=install_act_record.action_date,
            cryptography_version_id=cryptography_version_id,
            key_document_id=key_document.id,
            install_action_id=install_act_record.id,
        )

        return key_document

    @classmethod
    async def add_personal_keys(cls, form_data):
        action_date = format_date(form_data.happened_at)

        try:
            # Создание актовой записи
            install_act_record = await CActionServise.add(
                action_type=ActRecordTypes.KD_INSTALL,
                number=await CActionServise.get_free_action_number(action_date),
                reason=form_data.reason,
                reason_date=format_date(form_data.reason_date),
                performer_id=int(form_data.performer_id),
                action_date=action_date,
                head_commision_member_id=int(form_data.head_commision_member_id),
                commision_member_id=int(form_data.commision_member_id),
            )

            # Создание ключевого документа на весь
            # срок жизненного цикла СКЗИ при нажатом чекбоксе
            # key_document_is_unexpired в состоянии "on"
            if form_data.key_document_is_unexpired == "on":
                await KeyDocumentServise.add_unexpired_key(
                    serial=form_data.key_document_unexpired_serial,
                    cryptography_version_id=int(form_data.version_id),
                    carrier_id=int(form_data.key_document_unexpired_carrier_id),
                    owner_id=int(form_data.responsible_user_id),
                    equipment_id=form_data.equipment_id,
                    received_from=form_data.key_document_unexpired_received_from,
                    received_date=format_date(
                        form_data.key_document_unexpired_received_at
                    ),
                    install_act_record=install_act_record,
                    comment=form_data.comment,
                )

            # Создание ключевого документа, который сменяется
            # через определённый период при нажатом чекбоксе
            # key_document_is_expired в состоянии "on"
            if form_data.key_document_is_expired == "on":
                match form_data.key_document_expired_is_new:
                    case "True":
                        await KeyDocumentServise.add_expired_key(
                            serial=form_data.key_document_expired_serial,
                            cryptography_version_id=int(form_data.version_id),
                            carrier_id=int(form_data.key_document_expired_carrier_id),
                            owner_id=int(form_data.responsible_user_id),
                            equipment_id=form_data.equipment_id,
                            received_from=form_data.key_document_expired_received_from,
                            received_date=format_date(
                                form_data.key_document_expired_received_at
                            ),
                            install_act_record=install_act_record,
                            comment=form_data.comment,
                        )
                    case "False":
                        expired_kd = await KeyDocumentServise.get_by_id(
                            int(form_data.key_document_id)
                        )
                        # TODO update key values !!!

            await cls.db.commit()

            # Принудительный сброс состояния сессии
            cls.db.session.expire_all()
        except Exception as e:
            await cls.db.rollback()
            raise e

    @classmethod
    async def replace_personal_keys(cls, form_data):
        action_date = format_date(form_data.happened_at)

        try:
            # Создание актовой записи
            act_record = await CActionServise.add(
                action_type=ActRecordTypes.KD_REPLACE,
                number=await CActionServise.get_free_action_number(action_date),
                reason=replace_reasons[int(form_data.reason_id)],
                reason_date=format_date(form_data.reason_date),
                performer_id=int(form_data.performer_id),
                action_date=action_date,
                head_commision_member_id=int(form_data.head_commision_member_id),
                commision_member_id=int(form_data.commision_member_id),
            )

            # Выводимый ключевой документ
            remove_key_document = await KeyDocumentServise.get_by_id(
                int(form_data.remove_key_document_id)
            )

            # Создание ключевого документа
            new_key_document = await KeyDocumentServise.add_expired_key(
                serial=form_data.new_key_document_serial,
                cryptography_version_id=remove_key_document.cryptography_version_id,
                carrier_id=int(form_data.new_key_document_carrier_id),
                owner_id=remove_key_document.owner_id,
                equipment_id=remove_key_document.equipment_id,
                received_from=form_data.new_key_document_received_from,
                received_date=format_date(form_data.new_key_document_received_at),
                install_act_record=act_record,
                comment=form_data.comment,
            )

            # Вывод ключевого документа из эксплуатации
            await cls.remove_key(remove_key_document.id, act_record.id, action_date)

            await cls.db.commit()

            # Принудительный сброс состояния сессии
            cls.db.session.expire_all()
        except Exception as e:
            await cls.db.rollback()
            raise e

    @classmethod
    async def count_keys(cls):
        count_query = select(func.count(cls.model.id.distinct()))
        count = (await db.execute(count_query)).scalar() or 0
        return count

    @classmethod
    async def count_today_keys(cls):
        count_query = select(func.count(cls.model.id.distinct())).filter(
            func.DATE(cls.model.created_at) == date.today()
        )
        count = (await db.execute(count_query)).scalar() or 0
        return count

    @classmethod
    async def count_month_keys(cls):
        count_query = select(func.count(cls.model.id.distinct())).filter(
            extract("month", cls.model.created_at) == datetime.today().month
        )
        count = (await db.execute(count_query)).scalar() or 0
        return count
