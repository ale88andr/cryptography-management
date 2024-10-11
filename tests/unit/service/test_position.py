from models.staff import Position
from services.position import PositionServise


position = Position(name="Тестовая должность", is_leadership=False)


async def test_get():
    s_position = await PositionServise.get(1)
    assert s_position == position
