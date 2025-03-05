from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_USER_ADD_HEADER as add_page_header,
    ADMIN_USER_EDIT_HEADER as edit_page_header,
    ADMIN_USER_DESCRIPTION as hepl_text,
    ADMIN_USER_INDEX_HEADER as index_page_header,
    ADMIN_USER as app_prefix,
    ADMIN_USER_FORM_TPL as form_teplate,
    ADMIN_USER_LIST_TPL as list_teplate,
)
from core.config import templates
from core.utils import create_breadcrumbs, get_bool_from_checkbox, redirect, redirect_with_error, redirect_with_message
from dependencies.auth import get_current_admin, get_current_user
from forms.user import UserForm
from services.auth import get_password_hash
from services.users import UsersDAO
from services.employee import EmployeeServise
from models.users import User


router = APIRouter(prefix=app_prefix, tags=[hepl_text])
index_url = "get_users_admin"


# ========= Users =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_users_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    error: Optional[str] = None,
    user: User = Depends(get_current_user)
):
    records, counter, total_records, total_pages = (
        await UsersDAO.all_with_pagination(
            sort=sort, q=q, page=page, limit=limit
        )
    )

    return templates.TemplateResponse(
        list_teplate,
        {
            "request": request,
            "users": records,
            "counter": counter,
            "page_header": index_page_header,
            "page_header_help": hepl_text,
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": total_pages,
            "msg": msg,
            "error": error,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_page_header], [index_url]
            ),
            "user": user
        },
    )


@router.get("/add")
async def add_user_admin(request: Request, user: User = Depends(get_current_user)):
    employees = await EmployeeServise.all()
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "employees": employees,
            "page_header": add_page_header,
            "page_header_help": hepl_text,
            "is_create": True,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, add_page_header],
                [index_url, "add_user_admin"],
            ),
            "user": user
        },
    )


@router.post("/add")
async def create_user_admin(request: Request, user: User = Depends(get_current_user)):
    form = UserForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user = await UsersDAO.add(
                email=form.email,
                hashed_password=get_password_hash(form.password),
                is_password_temporary=True
            )

            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Пользователь '{user}' добавлен!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    context = {
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            [index_url, "add_user_admin"],
        ),
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{pk}/edit")
async def edit_user_admin(pk: int, request: Request, user: User = Depends(get_current_user)):
    edit_user = await UsersDAO.get_by_id(pk)
    employees = await EmployeeServise.all()
    return templates.TemplateResponse(
        form_teplate,
        {
            "request": request,
            "email": edit_user.email,
            "is_admin": edit_user.is_admin,
            "is_blocked": edit_user.is_blocked,
            "employee_id": edit_user.employee_id,
            "employees": employees,
            "page_header": edit_page_header,
            "page_header_help": hepl_text,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, edit_page_header],
                [index_url, "edit_user_admin"],
            ),
            "user": user
        },
    )


@router.post("/{pk}/edit")
async def update_user_admin(pk: int, request: Request, user: User = Depends(get_current_user)):
    form = UserForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await UsersDAO.update(
                pk,
                email=form.email,
                employee_id=form.employee_id,
                is_admin=get_bool_from_checkbox(form.is_admin),
                is_blocked=get_bool_from_checkbox(form.is_blocked),
            )
            if form.password:
                await UsersDAO.update(
                    pk,
                    hashed_password=get_password_hash(form.password),
                    is_password_temporary=True,
                )

            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Данные пользователя '{obj}' обновлены!"
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    employees = await EmployeeServise.all()
    context = {
        "request": request,
        "employees": employees,
        "page_header": edit_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, edit_page_header],
            [index_url, "edit_user_admin"],
        ),
        "user": user,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{pk}/delete")
async def delete_user_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
    user = await UsersDAO.get_by_id(pk)

    if not user:
        return redirect_with_error(request, index_url, "Пользователь не найден.")

    if user.is_admin:
        return redirect_with_error(request, index_url, "Удаление пользователей с ролью администратор запрещено!")

    try:
        await UsersDAO.delete(pk)
        return redirect_with_message(request, index_url, "Пользователь удален!")
    except Exception as e:
        return redirect_with_error(request, index_url, f"Необработанная ошибка удаления пользователя '{user}': {e}")
