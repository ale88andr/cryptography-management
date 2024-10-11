from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from api.v1.position import positions


router = APIRouter(prefix="/pages", tags=["Фронтенд"])

templates = Jinja2Templates(directory="src/templates")


# ========= Positions =========
@router.get("/positions")
async def get_positions_page(request: Request, data=Depends(positions)):
    return templates.TemplateResponse(
        name="positions.html", context={"request": request, "positions": data}
    )
