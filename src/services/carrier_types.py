from typing import Optional
from sqlalchemy import select, text, func
from db.connection import db

from services.base import BaseRepository
from models.cryptography import KeyCarrierType, KeyCarrier


class CarrierTypesServise(BaseRepository):
    model = KeyCarrierType

    @classmethod
    async def all(
        cls,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None
    ):
        query = select(cls.model)

        # Filter rows
        if filters:
            query = query.filter_by(**filters)

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.name.ilike(f"%{text(q)}%"))

        records = (await db.execute(query)).scalars().all()

        return records, len(records)
