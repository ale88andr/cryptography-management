from datetime import date
from typing import Optional, Union
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload, selectinload

from db.connection import db
from services.base import BaseRepository
from models.logbook import CryptographyPersonalAccount


class EmployeePersonalAccountService(BaseRepository):
    model = CryptographyPersonalAccount

    @classmethod
    async def all(cls, sort: str = None, filters: Optional[dict] = None):
        query = select(cls.model).options(
            joinedload(cls.model.cryptography_version),
            joinedload(cls.model.key_document),
            joinedload(cls.model.equipment),
        )

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if filters:
            query = query.filter_by(**filters)

        records = (await db.execute(query)).scalars().all()

        return records, len(records)

    @classmethod
    async def get_by_user(cls, user_id: int = None, only_active: bool = False):
        if user_id:
            query = (
                select(cls.model)
                .options(
                    joinedload(cls.model.cryptography_version),
                    joinedload(cls.model.key_document),
                    joinedload(cls.model.equipment),
                    joinedload(cls.model.install_action),
                    joinedload(cls.model.remove_action),
                )
                .filter_by(user_id=user_id)
            )

            if only_active:
                query = query.filter(cls.model.remove_action_id.is_(None))

            records = (await db.execute(query)).scalars().all()
            return records, len(records)
