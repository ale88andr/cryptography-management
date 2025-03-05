from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_EQUIPMENT_ADD_HEADER as add_page_header,
    ADMIN_EQUIPMENT_EDIT_HEADER as edit_page_header,
    ADMIN_EQUIPMENT_DESCRIPTION as hepl_text,
    ADMIN_EQUIPMENT_INDEX_HEADER as index_page_header,
    ADMIN_EQUIPMENT as app_prefix,
    ADMIN_EQUIPMENT_FORM_TPL as form_template,
    ADMIN_EQUIPMENT_DETAIL_TPL as detail_template,
    ADMIN_EQUIPMENT_HW_FORM_TPL as hw_form_template,
    ADMIN_EQUIPMENT_LIST_TPL as list_template,
)
from core.config import templates
from core.utils import create_breadcrumbs, create_file_response, redirect, redirect_with_error, redirect_with_message
from core.templater import LogbookTemplatesEnum
from dependencies.auth import get_current_admin
from forms.equipment import EquipmentForm
from forms.hwlog import HWLogbookForm
from services.c_version import CVersionServise
from services.equipment import EquipmentServise
from services.c_hardware_logbook import CHardwareLogbookServise
from models.logbook import RECORD_TYPES, HardwareLogbookRecordType
from models.users import User
from services.key_document import KeyDocumentServise
from utils.formatting import format_date


router = APIRouter(prefix=app_prefix, tags=[hepl_text])
index_url = "get_equipments_admin"


# ========= Equipments =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_equipments_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    error: Optional[str] = None,
    user: User = Depends(get_current_admin)
):
    records, counter, total_records, total_pages = (
        await EquipmentServise.all_with_pagination(
            sort=sort, q=q, page=page, limit=limit
        )
    )
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
        "error": error,
        "sort": sort,
        "q": q,
        "breadcrumbs": create_breadcrumbs(
            router, [index_page_header], [index_url]
        ),
        "user": user
    }
    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_equipment_admin(request: Request, user: User = Depends(get_current_admin)):
    context = {
        "request": request,
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            [index_url, "add_equipment_admin"],
        ),
        "user": user
    }
    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_equipment_admin(request: Request, user: User = Depends(get_current_admin)):
    form = EquipmentForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await EquipmentServise.add(
                id=form.id,
                serial=form.serial,
                description=form.description,
                sticker=form.sticker,
            )
            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Оборудование '{obj}' добавлено!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    context = {
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            [index_url, "add_equipment_admin"],
        ),
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{equipment_id}")
async def detail_equipment_admin(equipment_id: str, request: Request, user: User = Depends(get_current_admin)):
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
            [index_url, "detail_equipment_admin"],
        ),
        "user": user
    }
    return templates.TemplateResponse(detail_template, context)


@router.get("/{equipment_id}/edit")
async def edit_equipment_admin(equipment_id: str, request: Request, user: User = Depends(get_current_admin)):
    obj = await EquipmentServise.get_by_id(equipment_id)
    context = {
        "request": request,
        "page_header": edit_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, edit_page_header],
            [index_url, "edit_equipment_admin"],
        ),
        "user": user
    }
    context.update(obj.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.post("/{equipment_id}/edit")
async def update_equipment_admin(equipment_id: str, request: Request, user: User = Depends(get_current_admin)):
    form = EquipmentForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await EquipmentServise.update(
                equipment_id,
                description=form.description,
                serial=form.serial,
                sticker=form.sticker,
            )
            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Оборудование '{obj}' обновлено!"
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
            [index_url, "add_equipment_admin"],
        ),
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_equipment_admin(pk: str, request: Request, user: User = Depends(get_current_admin)):
    equipment = await EquipmentServise.get_by_id(pk)

    if not equipment:
        return redirect_with_error(request, index_url, "Оборудование не найдено.")

    keys = await KeyDocumentServise.all(equipment_id=equipment.id)

    if keys:
        key_serials = "; ".join([item.serial for item in keys])
        return redirect_with_error(
            request,
            index_url,
            f"Невозможно удалить оборудование '{equipment.id}', так как на нём зарегистрирована ключевая информация: {key_serials}, которая была учтена ранее!"
        )

    try:
        await EquipmentServise.delete(pk)
        return redirect_with_message(request, index_url, "Оборудование удалено!")
    except Exception as e:
        return redirect_with_error(
            request,
            index_url,
            f"Необработанная ошибка удаления модели СКЗИ '{equipment.id}': {e}"
        )


@router.get("/{equipment_id}/hw/add")
async def add_hardware_logbook_admin(equipment_id: str, request: Request, user: User = Depends(get_current_admin)):
    equipment = await EquipmentServise.get_by_id(equipment_id)
    versions, _ = await CVersionServise.get_list()
    add_hw_page_header = (
        f"Добавление записи аппаратного журнала оборудования '{equipment.id}'"
    )
    context = {
        "request": request,
        "equipment": equipment,
        "versions": versions,
        "record_types": [
            RECORD_TYPES[i] for i in range(len(RECORD_TYPES)) if i in [2, 5, 6, 7]
        ],
        "page_header": add_hw_page_header,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_hw_page_header],
            [index_url, "add_hardware_logbook_admin"],
        ),
        "user": user
    }
    return templates.TemplateResponse(hw_form_template, context)


@router.post("/{equipment_id}/hw/add")
async def add_hardware_logbook_admin(equipment_id: str, request: Request, user: User = Depends(get_current_admin)):
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
            return redirect(
                request=request,
                endpoint="detail_equipment_admin",
                msg=f"Запись аппаратного журнала добавлена!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    versions, _ = await CVersionServise.get_list()
    context = {
        "page_header": f"Добавление записи аппаратного журнала оборудования '{equipment_id}'",
        "page_header_help": hepl_text,
        "versions": versions,
        "record_types": RECORD_TYPES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            [index_url, "add_equipment_admin"],
        ),
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(hw_form_template, context)


@router.get("/{equipment_id}/hw/doc")
async def download_hardware_logbook_admin(equipment_id: str, request: Request, user: User = Depends(get_current_admin)):
    equipment = await EquipmentServise.get_by_id(equipment_id)
    items, _ = await CHardwareLogbookServise.get_by_equipment(equipment_id)

    return create_file_response(
        LogbookTemplatesEnum.HARDWARE_LOGBOOK.value,
        {"equipment": equipment, "items": items, "RT": RECORD_TYPES},
        f"Аппаратный журнал СКЗИ - {equipment.id}",
    )
