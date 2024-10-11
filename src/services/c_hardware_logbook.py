from datetime import date
from typing import Optional, Union
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

from db.connection import db
from services.base import BaseRepository
from models.logbook import HardwareLogbook, HardwareLogbookRecordType


class CHardwareLogbookServise(BaseRepository):
    model = HardwareLogbook

    @classmethod
    async def all(cls, sort: str = None, filters: Optional[dict] = None):
        query = select(cls.model).options(
            joinedload(cls.model.cryptography_version),
        )

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if filters:
            query = query.filter_by(**filters)

        records = (await db.execute(query)).scalars().all()

        return records, len(records)

    @classmethod
    async def get_by_equipment(cls, equipment_id: int = None):
        if equipment_id:
            query = select(cls.model).filter_by(equipment_id=equipment_id)
            records = (await db.execute(query)).scalars().all()
            return records, len(records)

    @classmethod
    async def add_record(
        cls,
        type_: HardwareLogbookRecordType,
        date_: date,
        equipment_id: int,
        version_id: Union[int, str],
        key_id: Union[int, str],
        comment: Optional[str] = None,
    ):
        return await cls.add(
            record_type=type_,
            happened_at=date_,
            equipment_id=equipment_id,
            cryptography_version_id=int(version_id),
            key_document_id=int(key_id),
            comment=comment,
        )
