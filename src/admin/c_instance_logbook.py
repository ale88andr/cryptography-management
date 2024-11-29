from dataclasses import asdict
from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    CILOG_HELP_TEXT as hepl_text,
    CILOG_INDEX_PAGE_HEADER as index_page_header,
    CILOG_ADD_PAGE_HEADER as add_page_header,
)
from core.config import templates
from core.templater import (
    DocumentTemplatesEnum,
    InstallKeyActDocumentContext,
    LogbookTemplatesEnum,
    UninstallKeyActDocumentContext,
)
from core.utils import create_breadcrumbs, create_file_response
from dependencies.auth import get_current_admin
from forms.c_instance_logbook import CInstanceLogbookAdd
from models.users import User
from services.c_instance_logbook import CInstanceLogbookServise
from services.c_version import CVersionServise
from services.employee import EmployeeServise
from services.equipment import EquipmentServise
from services.key_carrier import KeyCarrierServise
from services.key_document import KeyDocumentServise
from utils.formatting import format_date_to_str, get_date_tuple, get_str_now_date


app_prefix = "/admin/cryptography/klog"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Cryptography Models Versions =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cilogbook_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_model_id: Optional[int] = None,
    filter_grade: Optional[int] = None,
    user: User = Depends(get_current_admin)
):
    # filters = {}

    # if filter_model_id and filter_model_id > 0:
    #     filters["model_id"] = filter_model_id

    # if filter_grade:
    #     filters["grade"] = filter_grade

    records, counter, total_records, total_pages = (
        await KeyDocumentServise.all_with_pagination(
            sort=sort, q=q, page=page, limit=limit
        )
    )

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
        "filter_model_id": filter_model_id,
        "filter_grade": filter_grade,
        "msg": msg,
        "sort": sort,
        "q": q,
        "breadcrumbs": create_breadcrumbs(
            router, [index_page_header], ["get_clogbook_admin"]
        ),
        "user": user,
    }
    return templates.TemplateResponse(list_teplate, context)


@router.get("/add")
async def add_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    versions = await CVersionServise.all_used()
    equipments = await EquipmentServise.all()
    employees = await EmployeeServise.all()
    security_staff_members = await EmployeeServise.security_staff_members()
    leadership_members = await EmployeeServise.leadership_members()
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
    return templates.TemplateResponse(form_teplate, context)


@router.post("/add")
async def create_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    form = CInstanceLogbookAdd(request)
    await form.load_data()
    if await form.is_valid():
        try:
            await KeyDocumentServise.add_personal_keys(form)

            redirect_url = request.url_for("get_cilogbook_admin").include_query_params(
                msg=f"Установка СКЗИ учтена!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    versions, _ = await CVersionServise.all()
    equipments = await EquipmentServise.all()
    employees = await EmployeeServise.all()
    leadership_members = await EmployeeServise.leadership_members()
    security_staff_members = await EmployeeServise.security_staff_members()
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
    return templates.TemplateResponse(form_teplate, context)


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
    _, month, year = get_date_tuple(key.install_act.action_date)

    all_act_keys, _ = await KeyDocumentServise.all(
        filters={"install_act_record_id": key.install_act_record_id}
    )

    context = InstallKeyActDocumentContext(
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

    return create_file_response(
        DocumentTemplatesEnum.KD_INSTALL.value, asdict(context), key.install_act.number
    )


@router.get("/{key_id}/distruction/doc")
async def download_instance_destruction_act_admin(key_id: int, request: Request, user: User = Depends(get_current_admin)):
    key = await KeyDocumentServise.get_by_id(key_id)

    _, month, year = get_date_tuple(key.remove_act.action_date)

    all_act_keys, _ = await KeyDocumentServise.all(
        filters={"remove_act_record_id": key.remove_act_record_id}
    )

    context = UninstallKeyActDocumentContext(
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

    return create_file_response(
        key.remove_act.action_type.value, asdict(context), key.remove_act.number
    )


@router.get("/doc")
async def download_cilogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    objects, _ = await CInstanceLogbookServise.all()

    return create_file_response(
        LogbookTemplatesEnum.INSTANCE_LOGBOOK.value,
        {"items": objects},
        f"Журнал поэкземплярного учета СКЗИ на дату - {get_str_now_date()}",
    )
