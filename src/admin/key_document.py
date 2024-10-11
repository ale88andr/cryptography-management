from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    KD_HELP_TEXT as hepl_text,
    KD_INDEX_PAGE_HEADER as index_page_header,
    KD_DESTRUCTION_PAGE_HEADER as destruction_page_header,
    KD_C_DESTRUCTION_PAGE_HEADER as c_destruction_page_header
)
from core.config import templates
from core.utils import create_breadcrumbs
from forms.destruction import DestructionForm
from models.logbook import ActRecordTypes
from services.c_action import CActionServise
from services.key_carrier import KeyCarrierServise
from services.key_document import KeyDocumentServise
from services.carrier_types import CarrierTypesServise
from services.employee import EmployeeServise
from models.cryptography import CRYPTO_MODEL_TYPES
from models.cryptography import CPRODUCT_GRADES
from utils.formatting import format_date

app_prefix = "/admin/cryptography/keys"
form_teplate = f"{app_prefix}/form.html"
detail_tepmlate = f"{app_prefix}/detail.html"
destruction_tepmlate = f"{app_prefix}/destruction.html"
c_destruction_tepmlate = f"{app_prefix}/c_destruction.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Key Documents =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_key_documents_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_type_id: Optional[int] = None,
    filter_owner_id: Optional[int] = None,
    status: Optional[str] = None,
):
    filters = {}
    if filter_type_id and filter_type_id > 0:
        filters["type_id"] = filter_type_id

    if filter_owner_id and filter_owner_id > 0:
        filters["owner_id"] = filter_owner_id

    filter_removed, filter_installed = None, None
    if status == "installed":
        filter_installed = True
    elif status == "removed":
        filter_removed = True

    objects, counter, total_records, total_pages = await KeyDocumentServise.all_with_pagination(
        sort=sort,
        q=q,
        page=page,
        limit=limit,
        filters=filters,
        is_removed=filter_removed,
        is_installed=filter_installed
    )
    key_carriers, _ = await KeyCarrierServise.all()
    carrier_types, _ = await CarrierTypesServise.all()
    employees = await EmployeeServise.all()
    context={
        "request": request,
        "objects": objects,
        "counter": counter,
        "carrier_types": carrier_types,
        "key_carriers": key_carriers,
        "employees": employees,
        "total_records": total_records,
        "total_pages": total_pages,
        "filter_type_id": filter_type_id,
        "filter_owner_id": filter_owner_id,
        "page_header": index_page_header,
        "page_header_help": hepl_text,
        "page": page,
        "limit": limit,
        "msg": msg,
        "sort": sort,
        "status": status,
        "q": q,
        "breadcrumbs": create_breadcrumbs(router, [index_page_header], ["get_cversions_admin"])
    }

    return templates.TemplateResponse(list_teplate, context)


@router.get("/{pk}")
async def detail_key_document_admin(pk: int, request: Request):
    key = await KeyDocumentServise.get_by_id(pk)
    context = {
        "request": request,
        "key": key,
        "cryptography_types": CRYPTO_MODEL_TYPES,
        "cryptography_grades": CPRODUCT_GRADES,
        "page_header": key.serial,
        "page_header_help": hepl_text,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, key.serial],
            ["get_key_documents_admin", "detail_key_document_admin"]
        )
    }
    return templates.TemplateResponse(detail_tepmlate, context)


@router.get("/{pk}/destruction")
async def destruction_key_document_admin(pk: int, request: Request):
    key = await KeyDocumentServise.get_by_id(pk)
    security_staff_members = await EmployeeServise.security_staff_members()
    context = {
        "request": request,
        "key": key,
        "page_header": destruction_page_header,
        "page_header_help": hepl_text,
        "employees": security_staff_members,
        "head_commision_member_id": None,
        "commision_member_id": None,
        "performer_id": None,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, destruction_page_header],
            ["get_key_documents_admin", "destruction_key_document_admin"]
        )
    }
    return templates.TemplateResponse(destruction_tepmlate, context)


@router.post("/{pk}/destruction")
async def destruct_key_document_admin(pk: int, request: Request):
    key = await KeyDocumentServise.get_by_id(pk)
    form = DestructionForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            happenned_at = format_date(form.action_date)

            # Запись данных акта об изъятии
            log_action = await CActionServise.add_record(
                ActRecordTypes.KD_REMOVE,
                happenned_at,
                form.head_commision_member_id,
                form.commision_member_id,
                form.performer_id,
                form.reason,
                format_date(form.reason_date),
            )

            # Внесение данных об изъятии в журналы
            await KeyDocumentServise.destruct_key(key, log_action, happenned_at)

            redirect_url = request.url_for(
                "get_key_documents_admin"
            ).include_query_params(
                msg=f"Ключевой документ выведен из эксплуатации!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    security_staff_members = await EmployeeServise.security_staff_members()
    context = {
        "request": request,
        "key": key,
        "page_header": destruction_page_header,
        "page_header_help": hepl_text,
        "employees": security_staff_members,
        "head_commision_member_id": None,
        "commision_member_id": None,
        "performer_id": None,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, destruction_page_header],
            ["get_key_documents_admin", "decommissioning_cversion_admin"]
        )
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(destruction_tepmlate, context)


@router.get("/{pk}/c_destruction")
async def destruct_employee_cversion_admin(pk: int, request: Request):
    key = await KeyDocumentServise.get_by_id(pk)
    responsible_user_cryptography_keys, _ = await KeyDocumentServise.all(filters={
            "owner_id": key.owner_id,
            "cryptography_version_id": key.cryptography_version_id,
            "remove_act_record_id": None
    })
    security_staff_members = await EmployeeServise.security_staff_members()
    context = {
        "request": request,
        "key": key,
        "page_header": c_destruction_page_header,
        "page_header_help": hepl_text,
        "employees": security_staff_members,
        "responsible_user_cryptography_keys": responsible_user_cryptography_keys,
        "head_commision_member_id": None,
        "commision_member_id": None,
        "performer_id": None,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, c_destruction_page_header],
            ["get_key_documents_admin", "destruct_employee_cversion_admin"]
        )
    }
    return templates.TemplateResponse(c_destruction_tepmlate, context)


@router.post("/{pk}/c_destruction")
async def destruct_key_cversion_admin(pk: int, request: Request):
    key = await KeyDocumentServise.get_by_id(pk)
    user_cryptography_keys, _ = await KeyDocumentServise.all(
        filters={
            "owner_id": key.owner_id,
            "cryptography_version_id": key.cryptography_version_id,
            "remove_act_record_id": None
        }
    )
    form = DestructionForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            action_date = format_date(form.action_date)

            # Запись данных акта об изъятии
            log_action = await CActionServise.add_record(
                ActRecordTypes.I_REMOVE,
                action_date,
                form.head_commision_member_id,
                form.commision_member_id,
                form.performer_id,
                form.reason,
                format_date(form.reason_date),
            )

            await KeyDocumentServise.destruct_c_version(
                keys=user_cryptography_keys,
                act_record=log_action,
                action_date=action_date
            )

            redirect_url = request.url_for(
                "get_key_documents_admin"
            ).include_query_params(
                msg=f"СКЗИ выведено из эксплуатации!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            print("-------------------------------")
            print(e)
            print("-------------------------------")
            form.errors.setdefault("non_field_error", e)

    security_staff_members = await EmployeeServise.security_staff_members()
    context = {
        "request": request,
        "key": key,
        "page_header": destruction_page_header,
        "page_header_help": hepl_text,
        "employees": security_staff_members,
        "responsible_user_cryptography_keys": user_cryptography_keys,
        "head_commision_member_id": None,
        "commision_member_id": None,
        "performer_id": None,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, destruction_page_header],
            ["get_key_documents_admin", "decommissioning_cversion_admin"]
        )
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(c_destruction_tepmlate, context)


@router.get("/{pk}/edit")
async def edit_key_document_admin(pk: int, request: Request):
    pass
