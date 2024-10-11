from typing import Optional
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from db.connection import db
from services.base import BaseRepository
from models.cryptography import Model


class CModelServise(BaseRepository):
    model = Model

    @classmethod
    async def all(
        cls,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None
    ):
        query = select(cls.model).options(joinedload(cls.model.manufacturer))

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if filters:
            query = query.filter_by(**filters)

        if q:
            query = query.filter(cls.model.name.ilike(f"%{text(q)}%"))

        records = (await db.execute(query)).scalars().all()

        return records, len(records)
