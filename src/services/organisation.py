from sqlalchemy import select

from db.connection import db
from services.base import BaseRepository
from models.staff import Organisation


class OrganisationServise(BaseRepository):
    model = Organisation

    @classmethod
    async def all(cls):
        query = select(cls.model)
        record = (await db.execute(query)).scalars().first()
        return record
