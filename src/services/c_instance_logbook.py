import math
from typing import Optional
from sqlalchemy import select, text, func
from sqlalchemy.orm import joinedload

from db.connection import db
from models.cryptography import KeyCarrier, KeyDocument, Version
from services.base import BaseRepository
from models.logbook import ActRecord


class CInstanceLogbookServise(BaseRepository):
    model = KeyDocument

    @classmethod
    async def all(cls, sort: str = None, filters: Optional[dict] = None):
        query = select(cls.model).options(
            joinedload(cls.model.cryptography_version).options(
                joinedload(Version.model)
            ),
            joinedload(cls.model.key_document).options(
                joinedload(KeyDocument.key_carrier).joinedload(KeyCarrier.carrier_type)
            ),
            joinedload(cls.model.responsible_user),
            joinedload(cls.model.install_action).options(
                joinedload(ActRecord.performer)
            ),
            joinedload(cls.model.remove_action).options(
                joinedload(ActRecord.performer)
            ),
            joinedload(cls.model.remove_action),
        )

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if filters:
            query = query.filter_by(**filters)

        records = (await db.execute(query)).scalars().all()

        return records, len(records)

    @classmethod
    async def all_with_pagination(
        cls,
        page: int = 0,
        limit: int = 0,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None,
    ):
        query = select(cls.model).options(
            joinedload(cls.model.cryptography_version).options(
                joinedload(Version.model)
            ),
            joinedload(cls.model.equipment),
            joinedload(cls.model.owner),
            joinedload(cls.model.install_act).options(joinedload(ActRecord.performer)),
            joinedload(cls.model.remove_act).options(joinedload(ActRecord.performer)),
        )

        # Filter rows
        if filters:
            query = query.filter_by(**filters)

        if not sort:
            query = query.order_by(
                # cls.model.install_act.action_date.desc(),
                # cls.model.install_act_record_id
            )
        else:
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.surname.ilike(f"%{text(q)}%"))

        if limit:
            query = query.offset(page * limit).limit(limit)

        count_query = select(func.count(1)).select_from(cls.model)

        total_records = (await db.execute(count_query)).scalar() or 0
        total_pages = math.ceil(total_records / limit) if limit else 0

        records = (await db.execute(query)).scalars().all()

        return records, len(records), total_records, total_pages
