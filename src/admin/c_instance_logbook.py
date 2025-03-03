from dataclasses import asdict
from datetime import date, datetime
from typing import Any, Dict, Optional
from fastapi import APIRouter, Request, Depends, HTTPException, responses, status

from admin.constants import (
    ADMIN_CILOG_DESCRIPTION as hepl_text,
    ADMIN_CILOG_INDEX_HEADER as index_page_header,
    ADMIN_CILOG_ADD_HEADER as add_page_header,
    ADMIN_CILOG_CHANGE_HEADER as change_page_header,
    ADMIN_CILOG as app_prefix,
    ADMIN_CILOG_FORM_TPL as form_template,
    ADMIN_CILOG_LIST_TPL as list_template,
    ADMIN_CILOG_CHANGE_FORM_TPL as change_form_template,
    ADMIN_CILOG_CHANGE_REASONS as replace_reasons
)
from core.config import templates
from core.templater import (
    InstallKeyActDocumentContext,
    LogbookTemplatesEnum,
    ReplaceKeyActDocumentContext,
    UninstallKeyActDocumentContext,
)
from core.utils import create_breadcrumbs, create_file_response, redirect
from dependencies.auth import get_current_admin
from forms.c_instance_logbook import CInstanceLogbookAdd, CInstanceLogbookChange
from models.cryptography import KeyDocument
from models.logbook import ActRecordTypes
from models.users import User
from services.c_action import CActionServise
from services.c_instance_logbook import CInstanceLogbookServise
from services.c_version import CVersionServise
from services.carrier_types import CarrierTypesServise
from services.employee import EmployeeServise
from services.equipment import EquipmentServise
from services.key_carrier import KeyCarrierServise
from services.key_document import KeyDocumentServise
from services.organisation import OrganisationServise
from utils.formatting import format_date_to_str, get_date_tuple, get_str_now_date


router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# Преобразование строковых параметров даты в объекты date
def parse_date(date_str: Optional[str]) -> Optional[date]:
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid date format for {date_str}")
    return None


# Создание фильтров
def create_logbook_filters(
    owner: Optional[int] = None,
    carrier: Optional[int] = None,
    version: Optional[int] = None,
    performer: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    status: Optional[str] = None,
    term: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        key: value
        for key, value in {
            "owner_id": owner,
            "carrier_id": carrier,
            "version_id": version,
            "performer_id": performer,
            "date_from": date_from,
            "date_to": date_to,
            "is_active": status == "installed",
            "is_disable": status == "removed",
            "is_expired": term == "expired",
            "is_unexpired": term == "unexpired",
        }.items()
        if value is not None and (value > 0 if value is int else value != "")
    }


# ========= Cryptography Models Versions =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cilogbook_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_carrier: Optional[int] = None,
    filter_owner: Optional[int] = None,
    filter_version: Optional[int] = None,
    filter_performer: Optional[int] = None,
    filter_date_from: Optional[str] = None,
    filter_date_to: Optional[str] = None,
    term: Optional[str] = None,
    status: Optional[str] = None,
    user: User = Depends(get_current_admin)
):
    filter_date_from = parse_date(filter_date_from)
    filter_date_to = parse_date(filter_date_to)

    filters = create_logbook_filters(
        filter_owner,
        filter_carrier,
        filter_version,
        filter_performer,
        filter_date_from,
        filter_date_to,
        status,
        term
    )

    records, counter, total_records, total_pages = (
        await KeyDocumentServise.all_with_pagination(
            sort=sort, q=q, page=page, limit=limit, filters=filters
        )
    )

    key_carrier_set, _ = await KeyCarrierServise.all()
    employee_set = await EmployeeServise.all()
    version_set = await CVersionServise.all_used()
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)

    context = {
        "request": request,
        "objects": records,
        "counter": counter,
        "total_records": total_records,
        "total_pages": total_pages,
        "page_header": index_page_header,
        "add_page_header": add_page_header,
        "page": page,
        "limit": limit,
        "page_header_help": hepl_text,
        "msg": msg,
        "filter_carrier": filter_carrier,
        "filter_owner": filter_owner,
        "filter_version": filter_version,
        "filter_performer": filter_performer,
        "filter_date_from": filter_date_from,
        "filter_date_to": filter_date_to,
        "sort": sort,
        "status": status,
        "term": term,
        "q": q,
        "key_carriers": key_carrier_set,
        "security_staff_members": security_staff_members,
        "cryptography_versions": version_set,
        "employees": employee_set,
        "breadcrumbs": create_breadcrumbs(
            router, [index_page_header], ["get_clogbook_admin"]
        ),
        "user": user,
    }
    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    versions = await CVersionServise.all_used()
    equipments = await EquipmentServise.get_short_list()
    employees = await EmployeeServise.get_short_list()
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
    leadership_members = await EmployeeServise.get_short_list(is_leadership=True)
    carriers, _ = await KeyCarrierServise.all()
    context = {
        "request": request,
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "cryptography_versions": versions,
        "equipments": equipments,
        "carriers": carriers,
        "is_created": True,
        "employees": employees,
        "leadership_members": leadership_members,
        "security_staff_members": security_staff_members,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_cilogbook_admin", "add_cilogbook_admin"],
        ),
        "user": user,
    }
    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    form = CInstanceLogbookAdd(request)
    await form.load_data()
    if await form.is_valid():
        try:
            await KeyDocumentServise.add_personal_keys(form)

            return redirect(
                request=request,
                endpoint="get_cilogbook_admin",
                msg=f"Установка СКЗИ учтена!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    versions, _ = await CVersionServise.all()
    equipments = await EquipmentServise.get_short_list()
    employees = await EmployeeServise.get_short_list()
    leadership_members = await EmployeeServise.get_short_list(is_leadership=True)
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
    carriers, _ = await KeyCarrierServise.all()
    context = {
        "request": request,
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "cryptography_versions": versions,
        "equipments": equipments,
        "carriers": carriers,
        "is_created": True,
        "employees": employees,
        "security_staff_members": security_staff_members,
        "leadership_members": leadership_members,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_cilogbook_admin", "add_cilogbook_admin"],
        ),
        "user": user,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/replace")
async def change_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    key_document_set = await KeyDocumentServise.all_expired()
    employees = await EmployeeServise.get_short_list()
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
    leadership_members = await EmployeeServise.get_short_list(is_leadership=True)
    carriers, _ = await KeyCarrierServise.all()
    context = {
        "request": request,
        "page_header": change_page_header,
        "page_header_help": hepl_text,
        "key_document_set": key_document_set,
        "carriers": carriers,
        "employees": employees,
        "leadership_members": leadership_members,
        "security_staff_members": security_staff_members,
        "replace_reasons": replace_reasons,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, change_page_header],
            ["get_cilogbook_admin", "change_cilogbook_admin"],
        ),
        "user": user,
    }
    return templates.TemplateResponse(change_form_template, context)


@router.get("/replace/{pk}")
async def change_current_cilogbook_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
    key_document_set = await KeyDocumentServise.all_expired()
    employees = await EmployeeServise.get_short_list()
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
    leadership_members = await EmployeeServise.get_short_list(is_leadership=True)
    carriers, _ = await KeyCarrierServise.all()
    context = {
        "request": request,
        "page_header": change_page_header,
        "page_header_help": hepl_text,
        "key_document_set": key_document_set,
        "remove_key_document_id": pk,
        "carriers": carriers,
        "employees": employees,
        "leadership_members": leadership_members,
        "security_staff_members": security_staff_members,
        "replace_reasons": replace_reasons,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, change_page_header],
            ["get_cilogbook_admin", "change_cilogbook_admin"],
        ),
        "user": user,
    }
    return templates.TemplateResponse(change_form_template, context)


@router.post("/replace")
async def change_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    form = CInstanceLogbookChange(request)
    await form.load_data()
    if await form.is_valid():
        try:
            await KeyDocumentServise.replace_personal_keys(form)

            return redirect(
                request=request,
                endpoint="get_cilogbook_admin",
                msg="Смена ключевой информации произведена!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            raise e

    key_document_set = await KeyDocumentServise.all_expired()
    employees = await EmployeeServise.get_short_list()
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
    leadership_members = await EmployeeServise.get_short_list(is_leadership=True)
    carriers, _ = await KeyCarrierServise.all()
    context = {
        "request": request,
        "page_header": change_page_header,
        "page_header_help": hepl_text,
        "key_document_set": key_document_set,
        "carriers": carriers,
        "employees": employees,
        "leadership_members": leadership_members,
        "security_staff_members": security_staff_members,
        "replace_reasons": replace_reasons,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, change_page_header],
            ["get_cilogbook_admin", "change_cilogbook_admin"],
        ),
        "user": user,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(change_form_template, context)


@router.get("/{record_id}/delete")
async def delete_clogbook_admin(record_id: int, request: Request, user: User = Depends(get_current_admin)):
    redirect_url = request.url_for("get_clogbook_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await CInstanceLogbookServise.delete(record_id)
        redirect_url = redirect_url.include_query_params(msg="Запись журнала удалена!")
    except Exception as e:
        redirect_url = redirect_url.include_query_params(errors={"non_field_error": e})

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)


@router.get("/{key_id}/install/doc")
async def download_instance_creation_act_admin(key_id: int, request: Request, user: User = Depends(get_current_admin)):
    key = await KeyDocumentServise.get_by_id(key_id)

    if key.install_act.action_type == ActRecordTypes.KD_REPLACE:
        context = await __create_context_for_replace_act_admin(key, key.install_act_record_id)
    else:
        context = await __create_context_for_install_act_admin(key)

    return create_file_response(
        key.install_act.action_type.value, asdict(context), key.install_act.number
    )


@router.get("/{key_id}/distruction/doc")
async def download_instance_destruction_act_admin(key_id: int, request: Request, user: User = Depends(get_current_admin)):
    try:
        key = await KeyDocumentServise.get_by_id(key_id)

        if not key:
            raise HTTPException(status_code=404, detail="Key not found")

        if key.remove_act.action_type == ActRecordTypes.KD_REPLACE:
            context = await __create_context_for_replace_act_admin(key, key.remove_act_record_id)
        else:
            context = await __create_context_for_destruction_act_admin(key)

        return create_file_response(
            key.remove_act.action_type.value, asdict(context), key.remove_act.number
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def __create_context_for_install_act_admin(key: KeyDocument):
    """
    Логика создания контекста для акта установки КИ
    """
    _, month, year = get_date_tuple(key.install_act.action_date)

    all_act_keys, _ = await KeyDocumentServise.all(
        filters={"install_act_record_id": key.install_act_record_id}
    )

    return InstallKeyActDocumentContext(
        action_date=format_date_to_str(key.install_act.action_date),
        number=key.install_act.number,
        month=month,
        year=year,
        reason_num=key.install_act.reason,
        reason_date=format_date_to_str(key.install_act.reason_date),
        performer=key.install_act.performer.short_name,
        performer_position=key.install_act.performer.full_position,
        head_commision_member=key.install_act.head_commision_member.short_name,
        head_commision_member_position=key.install_act.head_commision_member.full_position,
        commision_member=key.install_act.commision_member.short_name,
        commision_member_position=key.install_act.commision_member.full_position,
        owner=key.owner.short_name,
        owner_full_name=key.owner.full_name,
        owner_position=key.owner.full_position,
        cryptography=key.cryptography_version,
        key_document_serials=list(
            map(lambda r: [r.key_carrier, r.serial], all_act_keys)
        ),
        location=key.owner.location,
        sticker=key.equipment.sticker if key.equipment.sticker else "",
        equipment=key.equipment_id,
    )


async def __create_context_for_destruction_act_admin(key: KeyDocument):
    """
    Логика создания контекста для акта удаления КИ
    """
    all_act_keys, _ = await KeyDocumentServise.all(
        filters={"remove_act_record_id": key.remove_act_record_id}
    )
    _, month, year = get_date_tuple(key.remove_act.action_date)

    return UninstallKeyActDocumentContext(
        action_date=format_date_to_str(key.remove_act.action_date),
        number=key.remove_act.number,
        month=month,
        year=year,
        reason_num=key.remove_act.reason,
        reason_date=format_date_to_str(key.remove_act.reason_date),
        performer=key.remove_act.performer.short_name,
        performer_position=key.remove_act.performer.full_position,
        head_commision_member=key.remove_act.head_commision_member.short_name,
        head_commision_member_position=key.remove_act.head_commision_member.full_position,
        commision_member=key.remove_act.commision_member.short_name,
        commision_member_position=key.remove_act.commision_member.full_position,
        owner=key.owner.short_name,
        owner_full_name=key.owner.full_name,
        owner_position=key.owner.full_position,
        owner_organisation=key.owner.organisation,
        cryptography=key.cryptography_version,
        key_document_serials=list(
            map(lambda r: [r.key_carrier, r.serial], all_act_keys)
        ),
        location=key.owner.location,
        equipment=key.equipment_id,
    )


async def __create_context_for_replace_act_admin(key: KeyDocument, record_id: int):
    """
    Логика создания контекста для акта замены КИ
    """
    remove_kd = await KeyDocumentServise.get_one_or_none(remove_act_record_id=record_id)
    add_kd = await KeyDocumentServise.get_one_or_none(install_act_record_id=record_id)
    org = await OrganisationServise.all()
    act = await CActionServise.get_by_id(record_id)
    _, month, year = get_date_tuple(act.action_date)

    return ReplaceKeyActDocumentContext(
        action_date=format_date_to_str(act.action_date),
        number=act.number,
        month=month,
        year=year,
        reason_num=act.reason,
        reason_date=format_date_to_str(act.reason_date),
        performer=act.performer.short_name,
        performer_position=act.performer.full_position,
        head_commision_member=act.head_commision_member.short_name,
        head_commision_member_position=act.head_commision_member.full_position,
        commision_member=act.commision_member.short_name,
        commision_member_position=act.commision_member.full_position,
        owner=key.owner.short_name,
        owner_full_name=key.owner.full_name,
        owner_position=key.owner.full_position,
        owner_organisation=key.owner.organisation,
        cryptography=key.cryptography_version,
        remove_key_document=remove_kd,
        add_key_document=add_kd,
        location=key.owner.location,
        equipment=key.equipment_id,
        org=org
    )

@router.get("/doc")
async def download_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    objects, _ = await CInstanceLogbookServise.all()

    return create_file_response(
        LogbookTemplatesEnum.INSTANCE_LOGBOOK.value,
        {"items": objects},
        f"Журнал поэкземплярного учета СКЗИ на дату - {get_str_now_date()}",
    )
