from typing import Dict, Optional
from fastapi import APIRouter, Request, Depends, responses, status
from admin.constants import (
    POS_ADD_PAGE_HEADER,
    POS_EDIT_PAGE_HEADER,
    POS_HELP_TEXT,
    POS_INDEX_PAGE_HEADER,
)

from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    get_bool_from_checkbox,
)
from dependencies.auth import get_current_admin
from forms.position import PositionForm
from models.users import User
from services.position import PositionServise


app_prefix = "/admin/staff/positions"
form_template = f"{app_prefix}/form.html"
list_template = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=["Должности сотрудников"])


def create_filters(is_leadership: Optional[str]) -> Dict[str, bool]:
    filters = {}
    if is_leadership is not None and is_leadership != "all":
        filters["is_leadership"] = True if is_leadership == "True" else False
    return filters


# ========= Positions =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_positions_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    columns: str = None,
    is_leadership: Optional[str] = None,
    user: User = Depends(get_current_admin),
):
    filters = create_filters(is_leadership)

    records, counter = await PositionServise.all(
        sort=sort, q=q, columns=columns, filters=filters
    )

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, POS_INDEX_PAGE_HEADER, POS_HELP_TEXT, user
    )
    context.update(
        {
            "positions": records,
            "counter": counter,
            "msg": msg,
            "is_leadership": is_leadership,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [POS_INDEX_PAGE_HEADER], ["get_positions_admin"]
            ),
        }
    )

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_position_admin(request: Request, user: User = Depends(get_current_admin)):
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, POS_ADD_PAGE_HEADER, POS_HELP_TEXT, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [POS_INDEX_PAGE_HEADER, POS_ADD_PAGE_HEADER],
                ["get_positions_admin", "add_position_admin"],
            ),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_position_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = PositionForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            position = await PositionServise.add(
                name=form.name, is_leadership=get_bool_from_checkbox(form.is_leadership)
            )
            redirect_url = request.url_for("get_positions_admin").include_query_params(
                msg=f"Должность '{position.name}' успешно создана!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, POS_ADD_PAGE_HEADER, POS_HELP_TEXT, user
    )
    context.update(form.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.get("/{position_id}/edit")
async def edit_position_admin(
    position_id: int, request: Request, user: User = Depends(get_current_admin)
):
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, POS_EDIT_PAGE_HEADER, POS_HELP_TEXT, user
    )

    position = await PositionServise.get_by_id(position_id)

    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [POS_INDEX_PAGE_HEADER, POS_EDIT_PAGE_HEADER],
                ["get_positions_admin", "edit_position_admin"],
            ),
            **vars(position),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/{position_id}/edit")
async def update_position_admin(
    position_id: int, request: Request, user: User = Depends(get_current_admin)
):
    form = PositionForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            position = await PositionServise.update(
                position_id,
                name=form.name,
                is_leadership=get_bool_from_checkbox(form.is_leadership),
            )
            redirect_url = request.url_for("get_positions_admin").include_query_params(
                msg=f"Должность '{position.name}' успешно обновлена!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, POS_EDIT_PAGE_HEADER, POS_HELP_TEXT, user
    )
    context.update(form.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_position_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    redirect_url = request.url_for("get_positions_admin")
    redirect_status = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await PositionServise.delete(pk)
        redirect = request.url_for("get_positions_admin").include_query_params(
            msg="Должность удалена!"
        )
        return responses.RedirectResponse(redirect, status_code=redirect_status)
    except Exception as e:
        redirect_url.include_query_params(errors={"non_field_error": e})
        return responses.RedirectResponse(redirect_url, status_code=redirect_status)
