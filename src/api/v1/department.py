from fastapi import APIRouter
from pydantic import BaseModel

from services.department import DepartmentServise


# Объект router, в котором регистрируем обработчики
router = APIRouter(prefix="/v1/departments", tags=["Отделы сотрудников"])


@router.get("")
async def departments():
    result = await DepartmentServise.get_all()
    return result
