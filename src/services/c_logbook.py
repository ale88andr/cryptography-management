from typing import Optional
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from db.connection import db
from models.cryptography import Version
from services.base import BaseRepository
from models.logbook import ActRecord


class CLogbookServise(BaseRepository):
    model = Version

    @classmethod
    async def all(cls, sort: str = None, filters: Optional[dict] = None):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.model),
                joinedload(cls.model.responsible_user),
                joinedload(cls.model.install_act).options(
                    joinedload(ActRecord.performer)
                ),
                joinedload(cls.model.remove_act).options(
                    joinedload(ActRecord.performer)
                ),
            )
            .join(ActRecord, cls.model.install_act)
        )

        if not sort and sort != "null":
            query = query.order_by(
                ActRecord.action_date.desc(), cls.model.install_act_record_id
            )
        else:
            query = query.order_by(text(sort))

        if filters:
            query = query.filter_by(**filters)

        records = (await db.execute(query)).scalars().all()

        return records, len(records)
