from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    DP_ADD_PAGE_HEADER as add_header,
    DP_EDIT_PAGE_HEADER as edit_header,
    DP_HELP_TEXT as help_text,
    DP_INDEX_PAGE_HEADER as index_header,
)
from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    redirect_with_error,
    redirect_with_message,
)
from dependencies.auth import get_current_admin
from forms.department import DepartmentForm
from models.users import User
from services.department import DepartmentServise


app_prefix = "/admin/staff/departments"
form_template = f"{app_prefix}/form.html"
list_template = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[help_text])


# ========= Departments =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_departments_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    user: User = Depends(get_current_admin),
):
    records, counter = await DepartmentServise.all(sort=sort, q=q)

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "departments": records,
            "counter": counter,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_header], ["get_departments_admin"]
            ),
        }
    )

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_department_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                ["get_departments_admin", "add_department_admin"],
            ),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_position_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = DepartmentForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            dept = await DepartmentServise.add(name=form.name)
            return redirect_with_message(
                request,
                "get_departments_admin",
                msg=f"Отдел '{dept.name}' создан!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{department_id}/edit")
async def edit_department_admin(
    department_id: int, request: Request, user: User = Depends(get_current_admin)
):
    dept = await DepartmentServise.get_by_id(department_id)
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_departments_admin", "edit_department_admin"],
            ),
            **vars(dept),
        }
    )
    return templates.TemplateResponse(form_template, context)


@router.post("/{department_id}/edit")
async def update_position_admin(
    department_id: int, request: Request, user: User = Depends(get_current_admin)
):
    form = DepartmentForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            dept = await DepartmentServise().update(department_id, name=form.name)
            return redirect_with_message(
                request,
                "get_departments_admin",
                msg=f"Отдел '{dept.name}' обновлен!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_departments_admin", "edit_department_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{department_id}/delete")
async def delete_department_admin(
    department_id: int, request: Request, user: User = Depends(get_current_admin)
):
    try:
        await DepartmentServise.delete(department_id)
        return redirect_with_message(
            request, "get_departments_admin", msg="Отдел удален!"
        )
    except Exception as e:
        return redirect_with_error(
            request, "get_departments_admin", errors={"non_field_error": str(e)}
        )
