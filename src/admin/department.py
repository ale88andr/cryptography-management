from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    DP_ADD_PAGE_HEADER,
    DP_EDIT_PAGE_HEADER,
    DP_HELP_TEXT,
    DP_INDEX_PAGE_HEADER,
)
from core.config import templates
from core.utils import add_breadcrumb
from services.department import DepartmentServise


app_prefix = "/admin/staff/departments"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[DP_HELP_TEXT])


# ========= Departments =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_departments_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
):
    records, counter = await DepartmentServise.all(sort=sort, q=q)
    return templates.TemplateResponse(
        list_teplate,
        context={
            "request": request,
            "departments": records,
            "counter": counter,
            "page_header": DP_INDEX_PAGE_HEADER,
            "page_header_help": DP_HELP_TEXT,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": [
                add_breadcrumb(
                    router,
                    DP_INDEX_PAGE_HEADER,
                    "get_departments_admin",
                    is_active=True,
                )
            ],
        },
    )


@router.get("/add")
async def add_department_admin(request: Request):
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header": DP_ADD_PAGE_HEADER,
            "page_header_help": DP_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, "Отделы сотрудников", "get_departments_admin"),
                add_breadcrumb(
                    router, DP_INDEX_PAGE_HEADER, "add_department_admin", is_active=True
                ),
            ],
        },
    )


@router.post("/add")
async def create_position_admin(request: Request):
    context = {
        "page_header_text": DP_ADD_PAGE_HEADER,
        "page_header_help_text": DP_HELP_TEXT,
    }
    form = DepartmentForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            dept = await DepartmentServise.add(name=form.name)
            redirect_url = request.url_for(
                "get_departments_admin"
            ).include_query_params(msg=f"Отдел '{dept.name}' создан!")
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{department_id}/edit")
async def edit_department_admin(department_id: int, request: Request):
    dept = await DepartmentServise.get_by_id(department_id)
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "name": dept.name,
            "page_header": DP_EDIT_PAGE_HEADER,
            "page_header_help": DP_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(
                    router, "Должности сотрудников", "get_departments_admin"
                ),
                add_breadcrumb(
                    router, DP_EDIT_PAGE_HEADER, "edit_department_admin", is_active=True
                ),
            ],
        },
    )


@router.post("/{department_id}/edit")
async def update_position_admin(department_id: int, request: Request):
    context = {
        "page_header_text": DP_EDIT_PAGE_HEADER,
        "page_header_help_text": DP_HELP_TEXT,
    }
    form = DepartmentForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            position = await DepartmentServise().update(
                department_id,
                name=form.name,
            )
            redirect_url = request.url_for(
                "get_departments_admin"
            ).include_query_params(msg=f"Отдел '{position.name}' обновлен!")
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{department_id}/delete")
async def delete_department_admin(department_id: int, request: Request):
    redirect_url = request.url_for("get_departments_admin")
    try:
        await DepartmentServise.delete(department_id)
        redirect = request.url_for("get_departments_admin").include_query_params(
            msg="Отдел удален!"
        )
        return responses.RedirectResponse(
            redirect, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    except Exception as e:
        redirect_url.include_query_params(errors={"non_field_error": e})
        return responses.RedirectResponse(
            redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )


class DepartmentForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict = {}
        self.name: str

    async def load_data(self):
        form = await self.request.form()
        self.name: str = form.get("name")

    async def is_valid(self):
        name_min_length = 3
        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if self.name:
            db_position = await DepartmentServise.get_one_or_none(name=self.name)
            if db_position:
                self.errors.setdefault(
                    "name", f"'{self.name}' - Такой отдел уже существует!"
                )
        if not self.errors:
            return True
        return False
