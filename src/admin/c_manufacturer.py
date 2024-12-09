from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    CM_ADD_PAGE_HEADER,
    CM_EDIT_PAGE_HEADER,
    CM_HELP_TEXT,
    CM_INDEX_PAGE_HEADER,
)
from core.config import templates
from core.utils import add_breadcrumb
from dependencies.auth import get_current_admin
from services.c_manufacturer import CManufacturerServise
from models.users import User

app_prefix = "/admin/cryptography/manufacturers"
form_template = f"{app_prefix}/form.html"
list_template = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[CM_HELP_TEXT])


# ========= Cryptography Manufacturers =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cmanufacturers_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    user: User = Depends(get_current_admin)
):
    records, counter = await CManufacturerServise.all(sort=sort, q=q)
    return templates.TemplateResponse(
        name=list_template,
        context={
            "request": request,
            "objects": records,
            "counter": counter,
            "page_header": CM_INDEX_PAGE_HEADER,
            "page_header_help": CM_HELP_TEXT,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": [
                add_breadcrumb(
                    router,
                    CM_INDEX_PAGE_HEADER,
                    "get_cmanufacturers_admin",
                    is_active=True,
                )
            ],
            "user": user,
        },
    )


@router.get("/add")
async def add_cmanufacturer_admin(request: Request, user: User = Depends(get_current_admin)):
    return templates.TemplateResponse(
        form_template,
        {
            "request": request,
            "page_header": CM_ADD_PAGE_HEADER,
            "page_header_help": CM_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(
                    router, CM_INDEX_PAGE_HEADER, "get_cmanufacturers_admin"
                ),
                add_breadcrumb(
                    router,
                    CM_ADD_PAGE_HEADER,
                    "add_cmanufacturer_admin",
                    is_active=True,
                ),
            ],
            "user": user,
        },
    )


@router.post("/add")
async def create_cmanufacturer_admin(request: Request, user: User = Depends(get_current_admin)):
    form = CManufacturerForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CManufacturerServise.add(name=form.name)
            redirect_url = request.url_for(
                "get_cmanufacturers_admin"
            ).include_query_params(msg=f"Производитель СКЗИ '{obj.name}' создан!")
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    context = {
        "page_header_text": CM_ADD_PAGE_HEADER,
        "page_header_help_text": CM_HELP_TEXT,
        "user": user,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.get("/{cm_id}/edit")
async def edit_cmanufacturer_admin(cm_id: int, request: Request, user: User = Depends(get_current_admin)):
    obj = await CManufacturerServise.get_by_id(cm_id)
    return templates.TemplateResponse(
        form_template,
        {
            "request": request,
            "name": obj.name,
            "page_header": CM_EDIT_PAGE_HEADER,
            "page_header_help": CM_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(
                    router, CM_INDEX_PAGE_HEADER, "get_cmanufacturers_admin"
                ),
                add_breadcrumb(
                    router,
                    CM_EDIT_PAGE_HEADER,
                    "edit_cmanufacturer_admin",
                    is_active=True,
                ),
            ],
            "user": user,
        },
    )


@router.post("/{cm_id}/edit")
async def update_carrier_admin(cm_id: int, request: Request, user: User = Depends(get_current_admin)):
    form = CManufacturerForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CManufacturerServise.update(
                cm_id,
                name=form.name,
            )
            redirect_url = request.url_for("get_carriers_admin").include_query_params(
                msg=f"Тип ключевого носителя '{obj.name}' обновлен!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    context = {
        "page_header_text": CM_EDIT_PAGE_HEADER,
        "page_header_help_text": CM_HELP_TEXT,
        "user": user,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.get("/{cm_id}/delete")
async def delete_cmanufacturer_admin(cm_id: int, request: Request, user: User = Depends(get_current_admin)):
    redirect_url = request.url_for("get_carriers_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await CManufacturerServise.delete(cm_id)
        redirect_url = redirect_url.include_query_params(
            msg="Ключевой носитель удален!"
        )
    except Exception as e:
        redirect_url = redirect_url.include_query_params(errors={"non_field_error": e})

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)


class CManufacturerForm:
    REQUIRED_ERROR = "Поле должно быть заполнено!"

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
            is_exists = await CManufacturerServise.get_one_or_none(name=self.name)
            if is_exists:
                self.errors.setdefault(
                    "name",
                    f"'{self.name}' - Производитель с таким именем уже существует!",
                )

        if not self.errors:
            return True
        return False
