import math
from typing import Optional
from sqlalchemy import select, text, func
from sqlalchemy.orm import joinedload, selectinload, subqueryload

from db.connection import db
from models.cryptography import KeyCarrier, KeyDocument, Version
from services.base import BaseRepository
from models.equipments import Equipment
from models.logbook import HardwareLogbook


class EquipmentServise(BaseRepository):
    model = Equipment

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await cls.db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def all_with_pagination(
        cls,
        page: int = 0,
        limit: int = 0,
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
            query = query.filter(cls.model.id.ilike(f"%{text(q)}%"))

        if limit:
            query = query.offset(page * limit).limit(limit)

        count_query = select(func.count(1)).select_from(cls.model)

        total_records = (await db.execute(count_query)).scalar() or 0
        total_pages = math.ceil(total_records/limit) if limit else 0

        records = (await db.execute(query)).scalars().all()

        return records, len(records), total_records, total_pages

    @classmethod
    async def get_by_id(cls, model_id: str):
        query = select(cls.model).options(
                selectinload(cls.model.hw_logs)
                .joinedload(HardwareLogbook.cryptography_version)
                .options(joinedload(Version.model)),
                selectinload(cls.model.hw_logs)
                .joinedload(HardwareLogbook.key_document)
                .options(joinedload(KeyDocument.key_carrier)
                         .options(joinedload(KeyCarrier.carrier_type))
                ),
                selectinload(cls.model.hw_logs)
                .subqueryload(HardwareLogbook.remove_action),
                selectinload(cls.model.key_documents)
                .options(joinedload(KeyDocument.cryptography_version))
            ).filter_by(id=model_id)
        result = await cls.db.execute(query)
        return result.scalar_one_or_none()
