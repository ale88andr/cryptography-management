import orjson

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.connection import Base
from models.common import fields


class Building(Base):
    __tablename__ = "employee_location_building"

    id: Mapped[fields.pk]
    name: Mapped[fields.title]
    city: Mapped[str] = mapped_column(String(20), nullable=False)
    street: Mapped[str] = mapped_column(String(40), nullable=False)
    building: Mapped[str] = mapped_column(String(5), nullable=False)
    index: Mapped[int]

    locations: Mapped[list["Location"]] = relationship(back_populates="building")

    @property
    def address(self):
        return f"г.{self.city}, ул.{self.street}, д.{self.building}"

    def __str__(self) -> str:
        return f"{self.name} ({self.address})"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class Location(Base):
    __tablename__ = "employee_location"
    __table_args__ = (
        UniqueConstraint("name", "building_id", name="name_building"),
    )

    id: Mapped[fields.pk]
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("employee_location_building.id", ondelete="CASCADE")
    )

    building: Mapped["Building"] = relationship(
        back_populates="locations", lazy="joined"
    )

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="location", lazy="selectin"
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.building.address})"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class Position(Base):
    __tablename__ = "employee_position"

    id: Mapped[fields.pk]
    name: Mapped[fields.title]
    is_leadership: Mapped[bool] = mapped_column(nullable=False, default=False)

    employees: Mapped[list["Employee"]] = relationship(back_populates="position")

    def __str__(self) -> str:
        return self.name

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class Department(Base):
    __tablename__ = "employee_department"

    id: Mapped[fields.pk]
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    employees: Mapped[list["Employee"]] = relationship(back_populates="department")

    def __str__(self) -> str:
        return self.name

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class Organisation(Base):
    __tablename__ = "employee_organisation"

    id: Mapped[fields.pk]
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    short_name: Mapped[fields.title]
    city: Mapped[str] = mapped_column(String(20), nullable=False)
    street: Mapped[str] = mapped_column(String(40), nullable=False)
    building: Mapped[str] = mapped_column(String(5), nullable=False)
    index: Mapped[int]
    chief: Mapped[str] = mapped_column(String(20), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(back_populates="organisation")

    @property
    def address(self):
        index = f", {self.index}" if self.index else ''
        return f"г.{self.city}, ул.{self.street}, д.{self.building}{index}"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[fields.pk]
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(30))
    is_worked: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_security_staff: Mapped[bool] = mapped_column(nullable=False, default=False)
    position_id: Mapped[int] = mapped_column(
        ForeignKey("employee_position.id", ondelete="CASCADE")
    )
    department_id: Mapped[int] = mapped_column(
        ForeignKey("employee_department.id", ondelete="CASCADE")
    )
    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("employee_organisation.id", ondelete="CASCADE")
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("employee_location.id", ondelete="CASCADE")
    )

    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

    # Relations
    position: Mapped["Position"] = relationship(back_populates="employees")

    user: Mapped["User"] = relationship(back_populates="employee")

    department: Mapped["Department"] = relationship(back_populates="employees")

    location: Mapped["Location"] = relationship(back_populates="employees")

    organisation: Mapped["Organisation"] = relationship(back_populates="employees")

    cryptography_set: Mapped[list["Version"]] = relationship(
        back_populates="responsible_user"
    )

    key_document_set: Mapped[list["KeyDocument"]] = relationship(back_populates="owner")

    @property
    def full_position(self):
        return f"{self.department}, {self.position}"

    @property
    def full_name(self):
        return f"{self.surname} {self.name} {self.middle_name}"

    @property
    def short_name(self):
        middle_name = f"{self.middle_name[0]}." if self.middle_name else ""
        return f"{self.surname} {self.name[0]}.{middle_name}"

    def __str__(self) -> str:
        return self.short_name

    def __repr__(self) -> str:
        return f"Сотрудник: #{self.id}"

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson.dumps
