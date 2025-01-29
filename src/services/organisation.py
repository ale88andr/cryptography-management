from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.connection import db
from services.base import BaseRepository
from models.staff import Employee, Organisation, Position


class OrganisationServise(BaseRepository):
    model = Organisation

    @classmethod
    async def all(cls):
        query = select(cls.model).options(
            joinedload(cls.model.responsible_employee).options(
                joinedload(Employee.position),
                joinedload(Employee.department)
            ),
            joinedload(cls.model.spare_responsible_employee).options(
                joinedload(Employee.position),
                joinedload(Employee.department)
            ),
            joinedload(cls.model.chief_employee).options(
                joinedload(Employee.position)
            ),
        )
        record = (await db.execute(query)).scalars().first()
        return record
