from sqlalchemy import delete, insert, select, update

from db.connection import db


class BaseRepository:
    """Базовый класс для сервисов"""

    model = None
    db = db

    @classmethod
    async def all(cls, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await cls.db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = select(cls.model).filter_by(id=int(model_id))
        result = await cls.db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await cls.db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        new_object = await cls.db.execute(query)
        await cls.db.commit()
        return new_object.scalar()

    @classmethod
    async def update(cls, id: int, **data):
        query = (
            update(cls.model)
            .where(cls.model.id == id)
            .values(**data)
            .returning(cls.model)
        )
        result = await cls.db.execute(query)
        await cls.db.commit()
        return result.scalar()

    @classmethod
    async def delete(cls, id: int):
        query = delete(cls.model).where(cls.model.id == id)
        await cls.db.execute(query)
        await cls.db.commit()
