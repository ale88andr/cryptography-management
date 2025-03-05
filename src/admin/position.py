from typing import Dict, Optional
from fastapi import APIRouter, Request, Depends, responses

from admin.constants import (
    ADMIN_POSITION_ADD_HEADER,
    ADMIN_POSITION_EDIT_HEADER,
    ADMIN_POSITION_DESCRIPTION,
    ADMIN_POSITION_INDEX_HEADER,
    ADMIN_POSITION as app_prefix,
    ADMIN_POSITION_FORM_TPL as form_template,
    ADMIN_POSITION_LIST_TPL as list_template,
)

from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    get_bool_from_checkbox,
    redirect,
    redirect_with_error,
    redirect_with_message
)
from dependencies.auth import get_current_admin
from forms.position import PositionForm
from models.users import User
from services.employee import EmployeeServise
from services.position import PositionServise


router = APIRouter(prefix=app_prefix, tags=[ADMIN_POSITION_INDEX_HEADER])
index_url = "get_positions_admin"


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
    error: Optional[str] = None,
    user: User = Depends(get_current_admin),
):
    filters = create_filters(is_leadership)

    records, counter = await PositionServise.all(
        sort=sort, q=q, columns=columns, filters=filters
    )

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_POSITION_INDEX_HEADER, ADMIN_POSITION_DESCRIPTION, user
    )
    context.update(
        {
            "positions": records,
            "counter": counter,
            "msg": msg,
            "error": error,
            "is_leadership": is_leadership,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [ADMIN_POSITION_INDEX_HEADER], [index_url]
            ),
        }
    )

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_position_admin(request: Request, user: User = Depends(get_current_admin)):
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_POSITION_ADD_HEADER, ADMIN_POSITION_DESCRIPTION, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [ADMIN_POSITION_INDEX_HEADER, ADMIN_POSITION_ADD_HEADER],
                [index_url, "add_position_admin"],
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
            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Должность '{position.name}' успешно создана!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_POSITION_ADD_HEADER, ADMIN_POSITION_DESCRIPTION, user
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{position_id}/edit")
async def edit_position_admin(
    position_id: int, request: Request, user: User = Depends(get_current_admin)
):
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_POSITION_EDIT_HEADER, ADMIN_POSITION_DESCRIPTION, user
    )

    position = await PositionServise.get_by_id(position_id)

    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [ADMIN_POSITION_INDEX_HEADER, ADMIN_POSITION_EDIT_HEADER],
                [index_url, "edit_position_admin"],
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
            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Должность '{position.name}' успешно обновлена!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_POSITION_EDIT_HEADER, ADMIN_POSITION_DESCRIPTION, user
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_position_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    position = await PositionServise.get_by_id(pk)

    if not position:
        return redirect_with_error(request, index_url, "Должность не найдена")

    employees = await EmployeeServise.all(position_id=position.id)

    if employees:
        employee_names = ", ".join([e.short_name for e in employees])
        return redirect_with_error(
            request,
            index_url,
            f"Невозможно удалить должность '{position}', сначала измените должности для связанных сотрудников: {employee_names}"
        )

    try:
        await PositionServise.delete(pk)
        return redirect_with_message(request, index_url, "Должность удалена!")
    except Exception as e:
        return redirect_with_error(
            request,
            index_url,
            f"Необработанная ошибка удаления '{position}': {e}"
        )
