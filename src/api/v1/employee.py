from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from core.exceptions import UserAddException
from services.employee import EmployeeServise
from dependencies.auth import get_current_admin, get_current_user
from models.users import User

# from services.employee import EmployeeService, get_employee_service


# Объект router, в котором регистрируем обработчики
router = APIRouter(prefix="/v1/employees", tags=["Сотрудники"])


class Employee(BaseModel):
    id: int
    name: str
    surname: str
    middle_name: str
    is_worked: bool
    position_id: int
    department_id: int
    organisation_id: int
    location_id: int


# @router.get("/{employee_id}", response_model=Employee)
# async def employee_details(
#     employee_id: str,
#     employee_service: EmployeeService = Depends(get_employee_service)
# ) -> Employee:
#     employee = await employee_service.get_by_id(employee_id)
#     if not employee:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

#     # Перекладываем данные из models.Film в Film
#     return Employee(id=employee.id, name=employee.title)


@router.get("/test")
async def test_request(user: User = Depends(get_current_user)):
    print(user, type(user), user.email)
    return user


@router.get("")
async def employees() -> list[Employee]:
    result = await EmployeeServise.get_all()
    return result


@router.get("/{employee_id}", response_model=Employee)
async def employee(employee_id):
    return {"id": employee_id, "name": "Test employee", "description": "Test"}


@router.post("")
async def add_employee(
    surname: str,
    name: str,
    middle_name: str,
    is_worked: bool,
    position_id: int,
    department_id: int,
    organisation_id: int,
    location_id: int,
    user: User = Depends(get_current_admin)
):
    employee: Employee = await EmployeeServise.add(
        surname, name, middle_name, is_worked, position_id, department_id, organisation_id, location_id,
    )
    if not employee:
        raise UserAddException
    return employee
