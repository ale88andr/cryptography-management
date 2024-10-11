from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    CARRIERS_ADD_PAGE_HEADER,
    CARRIERS_EDIT_PAGE_HEADER,
    CARRIERS_HELP_TEXT,
    CARRIERS_INDEX_PAGE_HEADER,
)
from core.config import templates
from core.utils import add_breadcrumb
from services.key_carrier import KeyCarrierServise
from services.carrier_types import CarrierTypesServise

app_prefix = "/admin/cryptography/carriers"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[CARRIERS_HELP_TEXT])


# ========= Carriers =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_carriers_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_type_id: Optional[int] = None,
):
    filters = {}
    if filter_type_id and filter_type_id > 0:
        filters["type_id"] = filter_type_id

    records, counter = await KeyCarrierServise.all(sort=sort, q=q, filters=filters)
    c_types, _ = await CarrierTypesServise.all()
    return templates.TemplateResponse(
        list_teplate,
        context={
            "request": request,
            "objects": records,
            "counter": counter,
            "carrier_types": c_types,
            "filter_type_id": filter_type_id,
            "page_header": CARRIERS_INDEX_PAGE_HEADER,
            "page_header_help": CARRIERS_HELP_TEXT,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": [
                add_breadcrumb(
                    router,
                    CARRIERS_INDEX_PAGE_HEADER,
                    "get_carriers_admin",
                    is_active=True,
                )
            ],
        },
    )


@router.get("/add")
async def add_carrier_admin(request: Request):
    c_types, _ = await CarrierTypesServise.all()
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header": CARRIERS_ADD_PAGE_HEADER,
            "page_header_help": CARRIERS_HELP_TEXT,
            "carrier_types": c_types,
            "breadcrumbs": [
                add_breadcrumb(
                    router, CARRIERS_INDEX_PAGE_HEADER, "get_carriers_admin"
                ),
                add_breadcrumb(
                    router, CARRIERS_ADD_PAGE_HEADER, "add_carrier_admin", is_active=True
                ),
            ],
        },
    )


@router.post("/add")
async def create_carrier_admin(request: Request):
    form = KeyCarrierForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await KeyCarrierServise.add(serial=form.serial, carrier_type_id=int(form.type_id))
            redirect_url = request.url_for("create_carrier_admin").include_query_params(
                msg=f"Ключевой носитель '{obj.serial}' создан!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    c_types, _ = await CarrierTypesServise.all()
    context = {
        "carrier_types": c_types,
        "page_header_text": CARRIERS_ADD_PAGE_HEADER,
        "page_header_help_text": CARRIERS_HELP_TEXT,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{carrier_id}/edit")
async def edit_carrier_admin(carrier_id: int, request: Request):
    obj = await KeyCarrierServise.get_by_id(carrier_id)
    c_types, _ = await CarrierTypesServise.all()
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "serial": obj.serial,
            "type_id": obj.carrier_type_id,
            "carrier_types": c_types,
            "page_header": CARRIERS_EDIT_PAGE_HEADER,
            "page_header_help": CARRIERS_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, CARRIERS_INDEX_PAGE_HEADER, "get_carriers_admin"),
                add_breadcrumb(router, CARRIERS_EDIT_PAGE_HEADER, "edit_carrier_admin", is_active=True),
            ],
        },
    )


@router.post("/{carrier_id}/edit")
async def update_carrier_admin(carrier_id: int, request: Request):
    form = KeyCarrierForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await KeyCarrierServise.update(
                carrier_id, name=form.name,
            )
            redirect_url = request.url_for(
                "get_carriers_admin"
            ).include_query_params(
                msg=f"Тип ключевого носителя '{obj.name}' обновлен!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context = {
        "page_header_text": CARRIERS_EDIT_PAGE_HEADER,
        "page_header_help_text": CARRIERS_HELP_TEXT,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{carrier_id}/delete")
async def delete_carrier_admin(carrier_id: int, request: Request):
    redirect_url = request.url_for("get_carriers_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await KeyCarrierServise.delete(carrier_id)
        redirect_url = redirect_url.include_query_params(
            msg="Ключевой носитель удален!"
        )
    except Exception as e:
        redirect_url = redirect_url.include_query_params(
            errors={"non_field_error": e}
        )

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)


class KeyCarrierForm:
    REQUIRED_ERROR = "Поле должно быть заполнено!"

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict = {}
        self.serial: str
        self.type_id: int

    async def load_data(self):
        form = await self.request.form()
        self.serial: str = form.get("serial")
        self.type_id: str = form.get("type_id")

    async def is_valid(self):
        name_min_length = 3
        if not self.serial or not len(self.serial) >= name_min_length:
            self.errors.setdefault(
                "serial", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if self.serial:
            is_exists = await KeyCarrierServise.get_one_or_none(serial=self.serial)
            if is_exists:
                self.errors.setdefault(
                    "serial", f"'{self.serial}' - Ключевой носитель с таким серийным номером уже существует!"
                )

        if not self.type_id or not self.type_id.isnumeric() or self.type_id == 0:
            self.errors.setdefault("type_id", self.REQUIRED_ERROR)

        if not self.errors:
            return True
        return False
