from datetime import date
from typing import Optional
from sqlalchemy import select, text, func
from sqlalchemy.orm import joinedload

from db.connection import db
from models.logbook import ActRecord, ActRecordTypes
from models.staff import Employee
from services.base import BaseRepository
from models.cryptography import KeyDocument, Model, Version
from services.c_action import CActionServise


class CVersionServise(BaseRepository):
    model = Version

    @classmethod
    async def get_list(cls, sort: str = None, q: str = None, filters: Optional[dict] = None):
        query = select(cls.model).options(
            joinedload(cls.model.responsible_user),
            joinedload(cls.model.model),
        )

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if filters:
            query = query.filter_by(**filters)

        if q:
            query = query.filter(cls.model.version.ilike(f"%{text(q)}%"))

        records = (await db.execute(query)).scalars().all()

        return records, len(records)

    @classmethod
    async def all_used(cls):
        query = (
            select(cls.model)
            .options(joinedload(cls.model.model))
            .filter(cls.model.remove_act_record_id.is_(None))
        )

        records = (await db.execute(query)).scalars().all()

        return records

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.install_act),
                joinedload(cls.model.model),
                joinedload(cls.model.responsible_user).options(
                    joinedload(Employee.position), joinedload(Employee.department)
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
    async def register(
        cls,
        version: str,
        model_id: int,
        grade_id: int,
        serial: str,
        dist_num: str,
        certificate: str,
        certificate_expired_at: date,
        received_num: str,
        received_from: str,
        received_at: date,
        form: str,
        license: str,
        responsible_user_id: int,
        comment: str,
        action_date: date,
    ):
        try:
            install_act_record = await CActionServise.add(
                action_type=ActRecordTypes.С_INSTALL,
                number=await CActionServise.get_free_action_number(action_date),
                performer_id=responsible_user_id,
                action_date=action_date,
            )

            await cls.add(
                version=version,
                model_id=model_id,
                grade_id=grade_id,
                serial=serial,
                dist_num=dist_num,
                certificate=certificate,
                certificate_expired_at=certificate_expired_at,
                received_num=received_num,
                received_from=received_from,
                received_at=received_at,
                form=form,
                license=license,
                responsible_user_id=responsible_user_id,
                comment=comment,
                install_act_record_id=install_act_record.id,
            )

            await cls.db.commit()
            await cls.db.session.flush()
        except Exception as e:
            print(
                f"--------- Exception in {cls.__class__.__name__}.register() ---------"
            )
            print(e)
            print(
                f"--------- Exception in {cls.__class__.__name__}.register() ---------"
            )
            await cls.db.rollback()

    @classmethod
    async def unregister(
        cls,
        version_id: int,
        head_commision_member_id: int,
        commision_member_id: int,
        performer_id: int,
        reason: str,
        action_date: date,
    ):
        try:
            remove_act_record = await CActionServise.add(
                action_type=ActRecordTypes.C_DESTRUCTION,
                number=await CActionServise.get_free_action_number(action_date),
                head_commision_member_id=head_commision_member_id,
                commision_member_id=commision_member_id,
                performer_id=performer_id,
                reason=reason,
                action_date=action_date,
            )

            await cls.update(version_id, remove_act_record_id=remove_act_record.id)

            await cls.db.commit()
            await cls.db.session.flush()
        except Exception as e:
            print(
                f"--------- Exception in {cls.__class__.__name__}.unregister() ---------"
            )
            print(e)
            print(
                f"--------- Exception in {cls.__class__.__name__}.unregister() ---------"
            )
            await cls.db.rollback()

    @classmethod
    async def count(cls) -> int:
        count_query = select(func.count(cls.model.id.distinct()))
        return (await db.execute(count_query)).scalar() or 0

    @classmethod
    async def count_unused(cls) -> int:
        count_query = select(func.count(cls.model.id.distinct())).filter(
            cls.model.remove_act_record_id.isnot(None)
        )
        count = (await db.execute(count_query)).scalar() or 0
        return count

    @classmethod
    async def count_by_versions(cls):
        query = (
            select(cls.model, func.count(cls.model.key_document_set))
            .join(KeyDocument, cls.model.key_document_set)
            .join(Model, cls.model.model)
            .group_by(cls.model)
        )
        result = (await db.execute(query)).fetchall()
        return result
