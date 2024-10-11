from typing import Optional
from sqlalchemy import select, text, func
from sqlalchemy.orm import joinedload

from db.connection import db
from services.base import BaseRepository
from models.cryptography import KeyCarrier, KeyDocument, KeyCarrierType


class KeyCarrierServise(BaseRepository):
    model = KeyCarrier

    @classmethod
    async def all(
        cls,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None
    ):
        query = select(cls.model).options(joinedload(cls.model.carrier_type))

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
    async def count_key_carriers(cls):
        query = select(
            KeyCarrierType.name,
            func.count(cls.model.key_documents)
        ).join(
            KeyDocument, cls.model.key_documents
        ).join(
            KeyCarrierType, cls.model.carrier_type
        ).group_by(
            cls.model,
            KeyCarrierType.name
        )
        result = (await db.execute(query)).fetchall()
        return result
