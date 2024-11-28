import math
from typing import Optional
from sqlalchemy import select, text, func
from sqlalchemy.orm import joinedload

from db.connection import db
from models.users import User
from services.base import BaseRepository


class UsersDAO(BaseRepository):
    model = User

    @classmethod
    async def all_with_pagination(
        cls,
        page: int = 0,
        limit: int = 0,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None,
    ):
        query = select(cls.model)

        # Filter rows
        if filters:
            query = query.filter_by(**filters)

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.email.ilike(f"%{text(q)}%"))

        if limit:
            query = query.offset(page * limit).limit(limit)

        count_query = select(func.count(1)).select_from(cls.model)

        total_records = (await db.execute(count_query)).scalar() or 0
        total_pages = math.ceil(total_records / limit) if limit else 0

        records = (await db.execute(query)).scalars().all()

        return records, len(records), total_records, total_pages
