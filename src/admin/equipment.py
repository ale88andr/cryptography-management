from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    EQ_ADD_PAGE_HEADER as add_page_header,
    EQ_EDIT_PAGE_HEADER as edit_page_header,
    EQ_HELP_TEXT as hepl_text,
    EQ_INDEX_PAGE_HEADER as index_page_header,
)
from core.config import templates
from core.utils import create_breadcrumbs, create_file_response
from core.templater import LogbookTemplatesEnum
from forms.equipment import EquipmentForm
from forms.hwlog import HWLogbookForm
from services.c_version import CVersionServise
from services.equipment import EquipmentServise
from services.c_hardware_logbook import CHardwareLogbookServise
from models.logbook import RECORD_TYPES, HardwareLogbookRecordType
from utils.formatting import format_date


app_prefix = "/admin/equipments"
form_teplate = f"{app_prefix}/form.html"
detail_teplate = f"{app_prefix}/detail.html"
hw_form_teplate = f"{app_prefix}/hw_form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Equipments =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_equipments_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None
):
    records, counter, total_records, total_pages = await EquipmentServise.all_with_pagination(sort=sort, q=q, page=page, limit=limit)
    context = {
        "request": request,
        "objects": records,
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
        "breadcrumbs": create_breadcrumbs(router, [index_page_header], ["get_cversions_admin"])
    }
    return templates.TemplateResponse(list_teplate, context)


@router.get("/add")
async def add_equipment_admin(request: Request):
    context = {
        "request": request,
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_equipments_admin", "add_equipment_admin"]
        )
    }
    return templates.TemplateResponse(form_teplate, context)


@router.post("/add")
async def create_equipment_admin(request: Request):
    form = EquipmentForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await EquipmentServise.add(
                id=form.id,
                serial=form.serial,
                description=form.description,
                sticker=form.sticker
            )
            redirect_url = request.url_for("get_equipments_admin").include_query_params(
                msg=f"Оборудование '{obj}' добавлено!"
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
            ["get_equipments_admin", "add_equipment_admin"]
        )
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{equipment_id}")
async def detail_equipment_admin(equipment_id: str, request: Request):
    equipment = await EquipmentServise.get_by_id(equipment_id)

    context = {
        "request": request,
        "equipment": equipment,
        "hardware_logbook_record_types": RECORD_TYPES,
        "page_header": equipment.id,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, equipment.id],
            ["get_equipments_admin", "detail_equipment_admin"]
        )
    }
    return templates.TemplateResponse(detail_teplate, context)


@router.get("/{equipment_id}/edit")
async def edit_equipment_admin(equipment_id: str, request: Request):
    obj = await EquipmentServise.get_by_id(equipment_id)
    context = {
        "request": request,
        "page_header": edit_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, edit_page_header],
            ["get_equipments_admin", "edit_equipment_admin"]
        )
    }
    context.update(obj.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.post("/{equipment_id}/edit")
async def update_equipment_admin(equipment_id: str, request: Request):
    form = EquipmentForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await EquipmentServise.update(
                equipment_id,
                description=form.description,
                serial=form.serial,
                sticker=form.sticker
            )
            redirect_url = request.url_for(
                "get_equipments_admin"
            ).include_query_params(
                msg=f"Оборудование '{obj}' обновлено!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    context = {
        "request": request,
        "page_header": edit_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, edit_page_header],
            ["get_equipments_admin", "add_equipment_admin"]
        )
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{equipment_id}/delete")
async def delete_equipment_admin(equipment_id: str, request: Request):
    redirect_url = request.url_for("get_equipments_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await EquipmentServise.delete(equipment_id)
        redirect_url = redirect_url.include_query_params(
            msg="Оборудование удалено!"
        )
    except Exception as e:
        redirect_url = redirect_url.include_query_params(
            errors={"non_field_error": e}
        )

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)


@router.get("/{equipment_id}/hw/add")
async def add_hardware_logbook_admin(equipment_id: str, request: Request):
    equipment = await EquipmentServise.get_by_id(equipment_id)
    versions, _ = await CVersionServise.all()
    add_hw_page_header = f"Добавление записи аппаратного журнала оборудования '{equipment.id}'"
    context = {
        "request": request,
        "equipment": equipment,
        "versions": versions,
        "record_types": [RECORD_TYPES[i] for i in range(len(RECORD_TYPES)) if i in [2, 5, 6, 7]],
        "page_header": add_hw_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_hw_page_header],
            ["get_equipments_admin", "add_hardware_logbook_admin"]
        )
    }
    return templates.TemplateResponse(hw_form_teplate, context)


@router.post("/{equipment_id}/hw/add")
async def add_hardware_logbook_admin(equipment_id: str, request: Request):
    form = HWLogbookForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            # Создание записи аппаратного журнала
            await CHardwareLogbookServise.add(
                record_type=HardwareLogbookRecordType(int(form.record_type)).name,
                equipment_id=equipment_id,
                happened_at=format_date(form.happened_at),
                cryptography_version_id=int(form.cryptography_version_id),
            )

            redirect_url = request.url_for(
                "detail_equipment_admin",
                equipment_id=equipment_id
            ).include_query_params(
                msg="Запись аппаратного журнала добавлена!"
            )

            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    versions, _ = await CVersionServise.all()
    context = {
        "page_header": f"Добавление записи аппаратного журнала оборудования '{equipment_id}'",
        "page_header_help": hepl_text,
        "versions": versions,
        "record_types": RECORD_TYPES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_equipments_admin", "add_equipment_admin"]
        )
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(hw_form_teplate, context)


@router.get("/{equipment_id}/hw/doc")
async def download_hardware_logbook_admin(equipment_id: str, request: Request):
    equipment = await EquipmentServise.get_by_id(equipment_id)
    items, _ = await CHardwareLogbookServise.get_by_equipment(equipment_id)

    return create_file_response(
        LogbookTemplatesEnum.HARDWARE_LOGBOOK.value,
        {"equipment": equipment, "items": items, "RT": RECORD_TYPES},
        f"Аппаратный журнал СКЗИ - {equipment.id}"
    )
