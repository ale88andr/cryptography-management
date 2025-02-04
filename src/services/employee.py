from datetime import date, datetime
from functools import lru_cache
import math
from typing import Optional
from sqlalchemy import select, text, func, extract
from sqlalchemy.orm import joinedload, selectinload, load_only

from db.connection import db
from models.cryptography import KeyCarrier, KeyDocument, Version
from models.logbook import ActRecord
from models.staff import Employee
from services.base import BaseRepository
from services.key_document import KeyDocumentServise

# EMPLOYEE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class EmployeeServise(BaseRepository):
    model = Employee

    @classmethod
    async def all_with_pagination(
        cls,
        page: int = 0,
        limit: int = 0,
        sort: str = None,
        q: str = None,
        filters: Optional[dict] = None,
    ):
        query = select(cls.model).options(
            joinedload(cls.model.position),
            joinedload(cls.model.department),
            joinedload(cls.model.location),
            joinedload(cls.model.organisation),
        )

        # Filter rows
        if filters:
            query = query.filter_by(**filters)

        if sort and sort != "null":
            query = query.order_by(text(sort))

        if q:
            query = query.filter(cls.model.surname.ilike(f"%{text(q)}%"))

        if limit:
            query = query.offset(page * limit).limit(limit)

        count_query = select(func.count(1)).select_from(cls.model)

        total_records = (await db.execute(count_query)).scalar() or 0
        total_pages = math.ceil(total_records / limit) if limit else 0

        records = (await db.execute(query)).scalars().all()

        return records, len(records), total_records, total_pages

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.position),
                joinedload(cls.model.department),
                joinedload(cls.model.location),
                joinedload(cls.model.organisation),
                selectinload(cls.model.key_document_set).options(
                    joinedload(KeyDocument.cryptography_version).options(
                        joinedload(Version.model)
                    ),
                    joinedload(KeyDocument.owner),
                    joinedload(KeyDocument.key_carrier).options(
                        joinedload(KeyCarrier.carrier_type)
                    ),
                    joinedload(KeyDocument.install_act).options(
                        joinedload(ActRecord.performer)
                    ),
                    joinedload(KeyDocument.remove_act).options(
                        joinedload(ActRecord.performer)
                    ),
                ),
            )
            .filter_by(id=int(model_id))
        )
        result = await cls.db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def latest_cryptography_users(cls, limit: int = None):
        query = (
            select(cls.model)
            .select_from(KeyDocument)
            .join(cls.model)
            .options(
                joinedload(cls.model.department),
                joinedload(cls.model.position),
                selectinload(cls.model.key_document_set).options(
                    joinedload(KeyDocument.cryptography_version).options(
                        joinedload(Version.model)
                    )
                ),
            )
            .where(KeyDocument.remove_act == None)
            .order_by(cls.model.created_at.desc())
        )
        records = (await db.execute(query)).unique().scalars().all()
        return records[:limit] if limit else records, len(records)

    @classmethod
    async def cryptography_users(
        cls, sort: str = None, q: str = None, filters: Optional[dict] = None
    ):
        query = (
            select(cls.model)
            .select_from(KeyDocument)
            .join(cls.model)
            .options(
                joinedload(cls.model.position),
                joinedload(cls.model.department),
                selectinload(cls.model.key_document_set).options(
                    joinedload(KeyDocument.cryptography_version).options(
                        joinedload(Version.model)
                    )
                ),
            )
            .where(KeyDocument.remove_act == None)
        )

        # Filter rows
        if filters:
            if filters.get("cryptography_version_id"):
                query = query.filter(
                    KeyDocument.cryptography_version_id
                    == filters["cryptography_version_id"]
                )
            else:
                query = query.filter_by(**filters)

        if q:
            query = query.filter(cls.model.surname.ilike(f"%{text(q)}%"))

        if sort and sort != "null":
            query = query.order_by(text(sort))
        else:
            query = query.order_by(cls.model.created_at.desc())

        records = (await db.execute(query)).unique().scalars().all()
        return records, len(records)

    @classmethod
    async def today_cryptography_users(cls):
        count_query = (
            select(func.count(cls.model.id.distinct()))
            .select_from(KeyDocument)
            .join(cls.model)
            .filter(func.DATE(cls.model.created_at) == date.today())
            .distinct()
        )
        today_users = (await db.execute(count_query)).scalar() or 0
        return today_users

    @classmethod
    async def month_cryptography_users(cls):
        count_query = (
            select(func.count(cls.model.id.distinct()))
            .select_from(KeyDocument)
            .join(cls.model)
            .filter(extract("month", cls.model.created_at) == datetime.today().month)
        )
        month_users = (await db.execute(count_query)).scalar() or 0
        return month_users

    @classmethod
    async def get_short_list(
        cls,
        is_leadership: bool = False,
        is_staff: bool = False,
        is_worked: bool = True,
    ):
        """Function used for HTML select lists options."""
        query = select(cls.model).options(load_only(
            cls.model.id,
            cls.model.name,
            cls.model.surname,
            cls.model.middle_name
        )).filter(
            cls.model.is_worked.is_(is_worked)
        )

        if is_staff:
            query = query.filter(cls.model.is_security_staff.is_(True))

        if is_leadership:
            query = query.filter(
                cls.model.position.has(is_leadership=is_leadership)
            )

        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def terminate_employee(
        cls, employee: Employee, keys: list[KeyDocument], act_record: ActRecord, action_date: date
    ):
        try:
            await cls.update(employee.id, is_worked=False)
            for key in keys:
                await KeyDocumentServise.remove_key(
                    key_id=key.id, act_record_id=act_record.id, action_date=action_date
                )
            await cls.db.commit()
            await cls.db.session.flush()
        except Exception as e:
            print(
                f"--------- Exception in {cls.__name__}.terminate_employee() ---------"
            )
            print(e)
            print(
                f"--------- Exception in {cls.__name__}.terminate_employee() ---------"
            )
            await cls.db.rollback()

    # @classmethod
    # async def add(
    #     cls,
    #     surname,
    #     name,
    #     middle_name,
    #     is_worked,
    #     position_id,
    #     department_id,
    #     organisation_id,
    #     location_id
    # ):
    #     async with async_session_maker() as session:
    #         query = insert(cls.model).values(
    #             surname=surname,
    #             name=name,
    #             middle_name=middle_name,
    #             is_worked=is_worked,
    #             position_id=position_id,
    #             department_id=department_id,
    #             organisation_id=organisation_id,
    #             location_id=location_id
    #         ).returning(cls.model)
    #         new_employee = await session.execute(query)
    #         await session.commit()
    #         return new_employee.scalar()


# EmployeeService содержит бизнес-логику по работе с фильмами.
# Никакой магии тут нет. Обычный класс с обычными методами.
# Этот класс ничего не знает про DI — максимально сильный и независимый.
# class EmployeeService:
#     def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
#         self.redis = redis
#         self.elastic = elastic

#     # get_by_id возвращает объект фильма. Он опционален,
#     # так как фильм может отсутствовать в базе
#     async def get_by_id(self, employee_id: str) -> Optional[Employee]:
#         # Пытаемся получить данные из кеша, потому что он работает быстрее
#         employee = await self._employee_from_cache(employee_id)
#         if not employee:
#             # Если фильма нет в кеше, то ищем его в Elasticsearch
#             employee = await self._get_employee_from_elastic(employee_id)

#         if not employee:
#             # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
#             return None

#         # Сохраняем фильм в кеш
#         await self._put_employee_to_cache(employee)
#         return employee

#     async def _get_employee_from_elastic(self, employee_id: str) -> Optional[Employee]:
#         doc = await self.elastic.get("movies", employee_id)
#         return Employee(**doc["_source"])

#     async def _employee_from_cache(self, employee_id: str) -> Optional[Employee]:
#         # Пытаемся получить данные о фильме из кеша, используя команду get
#         # https://redis.io/commands/get
#         data = await self.redis.get(employee_id)
#         if not data:
#             return None

#         # pydantic предоставляет удобное API для создания объекта моделей из json
#         employee = Employee.parse_raw(data)
#         return employee

#     async def _put_employee_to_cache(self, employee: Employee):
#         # Сохраняем данные о фильме, используя команду set
#         # Выставляем время жизни кеша — 5 минут
#         # https://redis.io/commands/set
#         # pydantic позволяет сериализовать модель в json
#         await self.redis.set(
#             employee.id, employee.json(), expire=EMPLOYEE_CACHE_EXPIRE_IN_SECONDS
#         )


# # get_employee_service — это провайдер EmployeeService.
# # С помощью Depends он сообщает, что ему необходимы Redis и Elasticsearch
# # Для их получения вы ранее создали функции-провайдеры в модуле db
# # Используем lru_cache-декоратор, чтобы создать объект сервиса
# # в едином экземпляре (синглтона)
# @lru_cache()
# def get_employee_service(
#     redis: Redis = Depends(get_redis),
#     elastic: AsyncElasticsearch = Depends(get_elastic),
# ) -> EmployeeService:
#     return EmployeeService(redis, elastic)
