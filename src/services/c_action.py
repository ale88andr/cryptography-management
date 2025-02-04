from datetime import date, datetime
from typing import Optional, Union
from sqlalchemy import select, text, func, extract, or_
from sqlalchemy.sql import functions

from db.connection import db
from services.base import BaseRepository
from models.logbook import ActRecord, ActRecordTypes


class CActionServise(BaseRepository):
    model = ActRecord

    @classmethod
    async def all(cls, sort: str = None, filters: Optional[dict] = None):
        query = select(cls.model)

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if filters:
            query = query.filter_by(**filters)

        records = (await db.execute(query)).scalars().all()

        return records, len(records)

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = select(cls.model).filter_by(id=int(model_id))
        result = await cls.db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_free_action_number(cls, action_date):
        count_query = (
            select(func.count(1))
            .filter(cls.model.action_date == action_date)
            .select_from(cls.model)
        )
        total_records = (await db.execute(count_query)).scalar() or 0
        return f'{action_date.strftime("%y%m%d")}-{total_records + 1}'

    @classmethod
    async def add_record(
        cls,
        type_: ActRecordTypes,
        date_: date,
        head_member_id: Union[int, str],
        member_id: Union[int, str],
        performer_id: Union[int, str],
        reason: Optional[str] = None,
        reason_date: Optional[date] = None,
    ):
        try:
            return await cls.add(
                action_type=type_,
                action_date=date_,
                number=await cls.get_free_action_number(date_),
                head_commision_member_id=int(head_member_id),
                commision_member_id=int(member_id),
                performer_id=int(performer_id),
                reason=reason,
                reason_date=reason_date,
            )
        except Exception as e:
            print(e)

    @classmethod
    async def count(cls) -> int:
        count_query = select(func.count(cls.model.id)).filter(
            extract("year", cls.model.created_at) >= datetime.today().year
        )
        return (await db.execute(count_query)).scalar() or 0

    @classmethod
    async def count_install(cls) -> int:
        count_query = (
            select(func.count(cls.model.id))
            .where(extract("year", cls.model.created_at) >= datetime.today().year)
            .filter(
                or_(
                    cls.model.action_type == ActRecordTypes.KD_INSTALL,
                    cls.model.action_type == ActRecordTypes.С_INSTALL,
                    cls.model.action_type == ActRecordTypes.I_INSTALL,
                )
            )
        )
        return (await db.execute(count_query)).scalar() or 0

    @classmethod
    async def count_remove(cls) -> int:
        count_query = (
            select(func.count(cls.model.id))
            .where(extract("year", cls.model.created_at) >= datetime.today().year)
            .filter(
                or_(
                    cls.model.action_type == ActRecordTypes.KD_REMOVE,
                    cls.model.action_type == ActRecordTypes.C_DESTRUCTION,
                    cls.model.action_type == ActRecordTypes.I_REMOVE,
                )
            )
        )
        return (await db.execute(count_query)).scalar() or 0

    @classmethod
    async def count_by_month(cls):
        query = (
            select(
                func.extract('month', cls.model.action_date),
                func.extract('year', cls.model.action_date),
                func.count(cls.model.id)
            )
            .filter(
                or_(
                    cls.model.action_type == ActRecordTypes.KD_INSTALL,
                    cls.model.action_type == ActRecordTypes.I_INSTALL,
                )
            )
            .group_by(
                func.extract('year', cls.model.action_date),
                func.extract('month', cls.model.action_date),
            ).order_by(
                func.extract('year', cls.model.action_date),
                func.extract('month', cls.model.action_date)
            ).limit(12)
        )
        return (await db.execute(query)).fetchall()
