from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from core.config import templates
from core.utils import add_breadcrumb
from dependencies.auth import get_current_admin
from models.users import User
from services.position import PositionServise


app_prefix = "/admin/staff/positions"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=["Должности сотрудников"])


# ========= Positions =========
@router.get("/positions", response_class=responses.HTMLResponse)
async def get_positions_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    columns: str = None,
    is_leadership: Optional[str] = None,
    user: User = Depends(get_current_admin)
):
    page_header_text = "Должности сотрудников"
    page_header_help_text = "Администрирование должностей сотрудников"

    filters = {}
    if is_leadership is not None and is_leadership != "all":
        filters["is_leadership"] = True if is_leadership == "True" else False

    records, counter = await PositionServise.all(
        sort=sort, q=q, columns=columns, filters=filters
    )
    return templates.TemplateResponse(
        list_teplate,
        context={
            "request": request,
            "positions": records,
            "counter": counter,
            "page_header_text": page_header_text,
            "page_header_help_text": page_header_help_text,
            "msg": msg,
            "is_leadership": is_leadership,
            "sort": sort,
            "q": q,
            "breadcrumbs": [
                add_breadcrumb(
                    router, page_header_text, "get_positions_admin", is_active=True
                )
            ],
            "user": user
        },
    )


@router.get("/positions/add")
async def add_position_admin(request: Request, user: User = Depends(get_current_admin)):
    page_header_text = "Добавление должности"
    page_header_help_text = "Администрирование должностей сотрудников"
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header_text": page_header_text,
            "page_header_help_text": page_header_help_text,
            "breadcrumbs": [
                add_breadcrumb(router, "Должности сотрудников", "get_positions_admin"),
                add_breadcrumb(
                    router, page_header_text, "add_position_admin", is_active=True
                ),
            ],
            "user": user
        },
    )


@router.post("/positions/add")
async def create_position_admin(request: Request, user: User = Depends(get_current_admin)):
    context = {
        "page_header_text": "Добавление должности",
        "page_header_help_text": "Администрирование должностей сотрудников",
        "user": user
    }
    form = PositionForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            position = await PositionServise.create(
                name=form.name, is_leadership=form.is_leadership
            )
            redirect_url = request.url_for("get_positions_admin").include_query_params(
                msg=f"Должность '{position.name}' успешно создана!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    print(context)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/positions/{position_id}/edit")
async def edit_position_admin(position_id: int, request: Request, user: User = Depends(get_current_admin)):
    page_header_text = "Редактирование должности"
    page_header_help_text = "Администрирование должностей сотрудников"
    position = await PositionServise.get_by_id(position_id)
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "name": position.name,
            "is_leadership": position.is_leadership,
            "page_header_text": page_header_text,
            "page_header_help_text": page_header_help_text,
            "breadcrumbs": [
                add_breadcrumb(router, "Должности сотрудников", "get_positions_admin"),
                add_breadcrumb(
                    router, page_header_text, "edit_position_admin", is_active=True
                ),
            ],
            "user": user
        },
    )


@router.post("/positions/{position_id}/edit")
async def update_position_admin(position_id: int, request: Request, user: User = Depends(get_current_admin)):
    context = {
        "page_header_text": "Редактирование должности",
        "page_header_help_text": "Администрирование должностей сотрудников",
        "user": user
    }
    form = PositionForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            position = await PositionServise.update(
                position_id, name=form.name, is_leadership=form.is_leadership
            )
            redirect_url = request.url_for("get_positions_admin").include_query_params(
                msg=f"Должность '{position.name}' успешно обновлена!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/positions/{position_id}/delete")
async def delete_position_admin(position_id: int, request: Request, user: User = Depends(get_current_admin)):
    redirect_url = request.url_for("get_positions_admin")
    try:
        await PositionServise.delete(model_id=position_id)
        redirect = request.url_for("get_positions_admin").include_query_params(
            msg="Должность удалена!"
        )
        return responses.RedirectResponse(
            redirect, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    except Exception as e:
        redirect_url.include_query_params(errors={"non_field_error": e})
        return responses.RedirectResponse(
            redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )


class PositionForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict = {}
        self.name: str
        self.is_leadership: bool = False

    async def load_data(self):
        form = await self.request.form()
        self.name: str = form.get("name")
        self.is_leadership: bool = True if form.get("is_leadership") == "on" else False

    async def is_valid(self):
        name_min_length = 3
        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if self.name:
            db_position = await PositionServise.get_one_or_none(name=self.name)
            if db_position:
                self.errors.setdefault(
                    "name", f"'{self.name}' - Такая должность уже существует!"
                )
        if not self.errors:
            return True
        return False
