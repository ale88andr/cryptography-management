from sqlalchemy import select, text

from db.connection import db
from services.base import BaseRepository
from models.staff import Department


class DepartmentServise(BaseRepository):
    model = Department

    @classmethod
    async def all(cls, sort: str = None, q: str = None):
        query = select(cls.model)

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.name.ilike(f"%{text(q)}%"))

        # print(str(query))
        records = (await db.execute(query)).scalars().all()

        return records, len(records)
