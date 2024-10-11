from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    CMODEL_ADD_PAGE_HEADER,
    CMODEL_EDIT_PAGE_HEADER,
    CMODEL_HELP_TEXT,
    CMODEL_INDEX_PAGE_HEADER,
)
from core.config import templates
from core.utils import create_breadcrumbs
from forms.c_model import CModelForm
from services.c_model import CModelServise
from services.c_manufacturer import CManufacturerServise
from models.cryptography import CRYPTO_MODEL_TYPES, ModelTypes

app_prefix = "/admin/cryptography/models"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[CMODEL_HELP_TEXT])


# ========= Cryptography Models =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cmodels_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_manufacturer_id: Optional[int] = None,
    filter_type: Optional[int] = None,
):
    filters = {}

    if filter_manufacturer_id and filter_manufacturer_id > 0:
        filters["manufacturer_id"] = filter_manufacturer_id

    if filter_type:
        filters["type"] = filter_type

    records, counter = await CModelServise.all(sort=sort, q=q, filters=filters)
    manufacturers, _ = await CManufacturerServise.all()
    context = {
        "request": request,
        "objects": records,
        "counter": counter,
        "page_header": CMODEL_INDEX_PAGE_HEADER,
        "page_header_help": CMODEL_HELP_TEXT,
        "types": CRYPTO_MODEL_TYPES,
        "manufacturers": manufacturers,
        "filter_manufacturer_id": filter_manufacturer_id,
        "filter_type": filter_type,
        "msg": msg,
        "sort": sort,
        "q": q,
        "breadcrumbs": create_breadcrumbs(
            router, [CMODEL_INDEX_PAGE_HEADER], ["get_cmodels_admin"]
        ),
    }
    return templates.TemplateResponse(list_teplate, context)


@router.get("/add")
async def add_cmodel_admin(request: Request):
    manufacturers, _ = await CManufacturerServise.all()
    context = {
        "request": request,
        "page_header": CMODEL_ADD_PAGE_HEADER,
        "page_header_help": CMODEL_HELP_TEXT,
        "manufacturers": manufacturers,
        "manufacturer_id": None,
        "type": None,
        "types": CRYPTO_MODEL_TYPES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [CMODEL_INDEX_PAGE_HEADER, CMODEL_ADD_PAGE_HEADER],
            ["get_cmodels_admin", "add_cmodel_admin"],
        ),
    }
    return templates.TemplateResponse(form_teplate, context)


@router.post("/add")
async def create_cmodel_admin(request: Request):
    form = CModelForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CModelServise.add(
                name=form.name,
                manufacturer_id=int(form.manufacturer_id),
                type=int(form.type),
                description=form.description,
            )
            redirect_url = request.url_for("get_cmodels_admin").include_query_params(
                msg=f"Модель СКЗИ '{obj.name}' создана!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    manufacturers, _ = await CManufacturerServise.all()
    context = {
        "page_header": CMODEL_INDEX_PAGE_HEADER,
        "page_header_help": CMODEL_HELP_TEXT,
        "manufacturers": manufacturers,
        "types": CRYPTO_MODEL_TYPES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [CMODEL_INDEX_PAGE_HEADER, CMODEL_ADD_PAGE_HEADER],
            ["get_cmodels_admin", "add_cmodel_admin"],
        ),
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{cmodel_id}/edit")
async def edit_cmodel_admin(cmodel_id: int, request: Request):
    obj = await CModelServise.get_by_id(cmodel_id)
    manufacturers, _ = await CManufacturerServise.all()
    context = {
        "request": request,
        "name": obj.name,
        "manufacturer_id": obj.manufacturer_id,
        "type": obj.type,
        "description": obj.description,
        "page_header": CMODEL_INDEX_PAGE_HEADER,
        "page_header_help": CMODEL_HELP_TEXT,
        "manufacturers": manufacturers,
        "types": CRYPTO_MODEL_TYPES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [CMODEL_INDEX_PAGE_HEADER, CMODEL_EDIT_PAGE_HEADER],
            ["get_cmodels_admin", "add_cmodel_admin"],
        ),
    }
    return templates.TemplateResponse(form_teplate, context)


@router.post("/{cmodel_id}/edit")
async def update_cmodel_admin(cmodel_id: int, request: Request):
    form = CModelForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            await CModelServise.update(
                cmodel_id,
                name=form.name,
                manufacturer_id=int(form.manufacturer_id),
                type=ModelTypes(int(form.type)),
                description=form.description,
            )
            redirect_url = request.url_for("get_cmodels_admin").include_query_params(
                msg=f"Модель СКЗИ обновлена!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    manufacturers, _ = await CManufacturerServise.all()
    context = {
        "page_header": CMODEL_EDIT_PAGE_HEADER,
        "page_header_help": CMODEL_HELP_TEXT,
        "manufacturers": manufacturers,
        "types": CRYPTO_MODEL_TYPES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [CMODEL_INDEX_PAGE_HEADER, CMODEL_EDIT_PAGE_HEADER],
            ["get_cmodels_admin", "add_cmodel_admin"],
        ),
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{cmodel_id}/delete")
async def delete_cmodel_admin(cmodel_id: int, request: Request):
    redirect_url = request.url_for("get_cmodels_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await CModelServise.delete(cmodel_id)
        redirect_url = redirect_url.include_query_params(msg="Модель СКЗИ удалена!")
    except Exception as e:
        redirect_url = redirect_url.include_query_params(errors={"non_field_error": e})

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)
