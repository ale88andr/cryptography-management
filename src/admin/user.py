from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    USR_ADD_PAGE_HEADER as add_page_header,
    USR_EDIT_PAGE_HEADER as edit_page_header,
    USR_HELP_TEXT as hepl_text,
    USR_INDEX_PAGE_HEADER as index_page_header,
)
from core.config import templates
from core.utils import create_breadcrumbs
from dependencies.auth import get_current_user
from forms.user import UserForm
from services.auth import get_password_hash
from services.users import UsersDAO
from services.employee import EmployeeServise
from models.users import User


app_prefix = "/admin/users"
form_teplate = f"{app_prefix}/form.html"
detail_teplate = f"{app_prefix}/detail.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Users =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_users_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
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
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_page_header], ["get_users_admin"]
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
                ["get_users_admin", "add_user_admin"],
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

            redirect_url = request.url_for("get_users_admin").include_query_params(
                msg=f"Пользователь '{user}' добавлен!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    context = {
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_users_admin", "add_user_admin"],
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
            "employee_id": edit_user.employee_id,
            "employees": employees,
            "page_header": edit_page_header,
            "page_header_help": hepl_text,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, edit_page_header],
                ["get_users_admin", "edit_user_admin"],
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
                employee_id=int(form.employee_id),
                is_admin=True if form.is_admin == "on" else False,
            )
            redirect_url = request.url_for("get_users_admin").include_query_params(
                msg=f"Данные пользователя '{obj}' обновлены!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
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
            ["get_users_admin", "edit_user_admin"],
        ),
        "user": user,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)
