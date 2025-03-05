from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_DEPARTMENT_ADD_HEADER as add_header,
    ADMIN_DEPARTMENT_EDIT_HEADER as edit_header,
    ADMIN_DEPARTMENT_DESCRIPTION as help_text,
    ADMIN_DEPARTMENT_INDEX_HEADER as index_header,
    ADMIN_DEPARTMENT as app_prefix,
    ADMIN_DEPARTMENT_FORM_TPL as form_template,
    ADMIN_DEPARTMENT_LIST_TPL as list_template,
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
from services.employee import EmployeeServise


router = APIRouter(prefix=app_prefix, tags=[help_text])
index_url = "get_departments_admin"


# ========= Departments =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_departments_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    error: Optional[str] = None,
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
            "error": error,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_header], [index_url]
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
                [index_url, "add_department_admin"],
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
                index_url,
                msg=f"Подразделение '{dept.name}' создано.",
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
    context.update({
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, edit_header],
            [index_url, "edit_department_admin"],
        ),
        **vars(dept),
    })
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
                index_url,
                msg=f"Подразделение '{dept.name}' обновлено.",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update({
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, edit_header],
            [index_url, "edit_department_admin"],
        )
    })
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_department_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    dept = await DepartmentServise.get_by_id(pk)

    if not dept:
        return redirect_with_error(request, index_url, "Подразделение не найдено")

    employees = await EmployeeServise.all(department_id=dept.id)

    if employees:
        employee_names = ", ".join([e.short_name for e in employees])
        return redirect_with_error(
            request,
            index_url,
            f"Невозможно удалить подразделение '{dept}', так как оно назначено следующим сотрудникам: {employee_names}"
        )

    if dept:
        try:
            await DepartmentServise.delete(pk)
            return redirect_with_message(request, index_url, "Подразделение удалено!")
        except Exception as e:
            return redirect_with_error(
                request,
                index_url,
                f"Необработанная ошибка удаления подразделения '{dept}': {e}"
            )
