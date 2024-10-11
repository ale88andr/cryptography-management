from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    CTYPES_ADD_PAGE_HEADER,
    CTYPES_EDIT_PAGE_HEADER,
    CTYPES_FORM_TEMPLATE,
    CTYPES_HELP_TEXT,
    CTYPES_INDEX_PAGE_HEADER,
)
from core.config import templates
from core.utils import add_breadcrumb
from services.carrier_types import CarrierTypesServise


app_prefix = "/admin/cryptography/carriers/types"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[CTYPES_HELP_TEXT])


# ========= Carrier types =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_ctypes_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
):
    records, counter = await CarrierTypesServise.all(sort=sort, q=q)
    return templates.TemplateResponse(
        list_teplate,
        context={
            "request": request,
            "objects": records,
            "counter": counter,
            "page_header": CTYPES_INDEX_PAGE_HEADER,
            "page_header_help": CTYPES_HELP_TEXT,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": [
                add_breadcrumb(
                    router,
                    CTYPES_INDEX_PAGE_HEADER,
                    "get_ctypes_admin",
                    is_active=True,
                )
            ],
        },
    )


@router.get("/add")
async def add_ctype_admin(request: Request):
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header": CTYPES_ADD_PAGE_HEADER,
            "page_header_help": CTYPES_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(
                    router, CTYPES_INDEX_PAGE_HEADER, "get_ctypes_admin"
                ),
                add_breadcrumb(
                    router, CTYPES_ADD_PAGE_HEADER, "add_ctype_admin", is_active=True
                ),
            ],
        },
    )


@router.post("/add")
async def create_ctype_admin(request: Request):
    form = CtypeForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CarrierTypesServise.add(name=form.name)
            redirect_url = request.url_for("get_ctypes_admin").include_query_params(
                msg=f"Тип ключевого носителя '{obj.name}' создан!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(CTYPES_FORM_TEMPLATE, form.__dict__)
    context = {
        "page_header_text": CTYPES_ADD_PAGE_HEADER,
        "page_header_help_text": CTYPES_HELP_TEXT,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{ctype_id}/edit")
async def edit_ctype_admin(ctype_id: int, request: Request):
    obj = await CarrierTypesServise.get_by_id(ctype_id)
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "name": obj.name,
            "page_header": CTYPES_EDIT_PAGE_HEADER,
            "page_header_help": CTYPES_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, CTYPES_INDEX_PAGE_HEADER, "get_ctypes_admin"),
                add_breadcrumb(router, CTYPES_EDIT_PAGE_HEADER, "edit_ctype_admin", is_active=True),
            ],
        },
    )


@router.post("/{ctype_id}/edit")
async def update_ctype_admin(ctype_id: int, request: Request):
    form = CtypeForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CarrierTypesServise.update(
                ctype_id, name=form.name,
            )
            redirect_url = request.url_for(
                "get_ctypes_admin"
            ).include_query_params(
                msg=f"Тип ключевого носителя '{obj.name}' обновлен!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(CTYPES_FORM_TEMPLATE, form.__dict__)
    context = {
        "page_header_text": CTYPES_EDIT_PAGE_HEADER,
        "page_header_help_text": CTYPES_HELP_TEXT,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{ctype_id}/delete")
async def delete_ctype_admin(ctype_id: int, request: Request):
    redirect_url = request.url_for("get_ctypes_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await CarrierTypesServise.delete(ctype_id)
        redirect_url = redirect_url.include_query_params(
            msg="Тип ключевого носителя удален!"
        )
    except Exception as e:
        redirect_url = redirect_url.include_query_params(
            errors={"non_field_error": e}
        )

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)


class CtypeForm:
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
            db_position = await CarrierTypesServise.get_one_or_none(name=self.name)
            if db_position:
                self.errors.setdefault(
                    "name", f"'{self.name}' - Такой тип ключевого носителя уже существует!"
                )
        if not self.errors:
            return True
        return False
