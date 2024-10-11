from typing import Optional
from sqlalchemy import select, text
from db.connection import db
from services.base import BaseRepository
from models.staff import Position


class PositionServise(BaseRepository):
    model = Position

    @classmethod
    async def all(
        cls,
        columns: str = None,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None
    ):
        query = select(cls.model)

        # Select columns
        # if columns:
        #     load_columns = [getattr(cls.model, c) for c in columns.split("-")]

        #     if load_columns and columns != "*":
        #         query = query.options(load_only(*load_columns))

        # Filter rows
        if filters:
            query = query.filter_by(**filters)

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.name.ilike(f"%{text(q)}%"))

        records = (await db.execute(query)).scalars().all()

        return records, len(records)
