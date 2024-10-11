from fastapi import APIRouter

from services.position import PositionServise
from schemas.position import SPosition


# Объект router, в котором регистрируем обработчики
router = APIRouter(prefix="/v1/positions", tags=["Должности сотрудников"])


@router.get("")
async def positions() -> list[SPosition]:
    result = await PositionServise.get_all()
    return result


@router.get("/{position_id}")
async def position(position_id):
    result = await PositionServise.get(position_id)
    return result
