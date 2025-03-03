from typing import Any, Dict, Optional
from fastapi import APIRouter, Request, Depends, responses

from admin.constants import (
    ADMIN_KEYDOC_DESCRIPTION as hepl_text,
    ADMIN_KEYDOC_INDEX_HEADER as index_page_header,
    ADMIN_KEYDOC_DESTRUCT_HEADER as destruction_page_header,
    ADMIN_KEYDOC_DESTRUCT_CRYPTO_HEADER as c_destruction_page_header,
    ADMIN_KEYDOC as app_prefix,
    ADMIN_KEYDOC_FORM_TPL as form_teplate,
    ADMIN_KEYDOC_DETAIL_TPL as detail_tepmlate,
    ADMIN_KEYDOC_DESTRUCT_TPL as destruction_tepmlate,
    ADMIN_KEYDOC_DESTRUCT_CRYPTO_TPL as c_destruction_tepmlate,
    ADMIN_KEYDOC_LIST_TPL as list_template,
)
from core.config import templates
from core.utils import create_breadcrumbs, redirect
from dependencies.auth import get_current_admin
from forms.destruction import DestructionForm
from models.logbook import ActRecordTypes
from services.c_action import CActionServise
from services.key_carrier import KeyCarrierServise
from services.key_document import KeyDocumentServise
from services.carrier_types import CarrierTypesServise
from services.employee import EmployeeServise
from models.cryptography import CRYPTO_MODEL_TYPES
from models.cryptography import CPRODUCT_GRADES
from models.users import User
from utils.formatting import format_date


router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# Создание фильтров сотрудников для методов: get_employees_admin, get_cusers_admin
def create_kd_filters(
    owner: Optional[int] = None,
    carrier: Optional[int] = None,
    status: Optional[str] = None,
    term: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        key: value
        for key, value in {
            "owner_id": owner,
            "carrier_id": carrier,
            "is_active": status == "installed",
            "is_disable": status == "removed",
            "is_expired": term == "expired",
            "is_unexpired": term == "unexpired",
        }.items()
        if value is not None and value > 0
    }


# ========= Key Documents =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_key_documents_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_carrier: Optional[int] = None,
    filter_owner: Optional[int] = None,
    term: Optional[str] = None,
    status: Optional[str] = None,
    user: User = Depends(get_current_admin)
):
    filters = create_kd_filters(filter_owner, filter_carrier, status, term)

    objects, counter, total_records, total_pages = (
        await KeyDocumentServise.all_with_pagination(
            sort=sort,
            q=q,
            page=page,
            limit=limit,
            filters=filters,
        )
    )
    key_carriers, _ = await KeyCarrierServise.all()
    carrier_types, _ = await CarrierTypesServise.all()
    employees = await EmployeeServise.all()
    context = {
        "request": request,
        "objects": objects,
        "counter": counter,
        "carrier_types": carrier_types,
        "key_carriers": key_carriers,
        "employees": employees,
        "total_records": total_records,
        "total_pages": total_pages,
        "filter_carrier": filter_carrier,
        "filter_owner": filter_owner,
        "page_header": index_page_header,
        "page_header_help": hepl_text,
        "page": page,
        "limit": limit,
        "msg": msg,
        "sort": sort,
        "status": status,
        "term": term,
        "q": q,
        "breadcrumbs": create_breadcrumbs(
            router, [index_page_header], ["get_cversions_admin"]
        ),
        "user": user
    }

    return templates.TemplateResponse(list_template, context)


@router.get("/{pk}")
async def detail_key_document_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
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
            ["get_key_documents_admin", "detail_key_document_admin"],
        ),
        "user": user
    }
    return templates.TemplateResponse(detail_tepmlate, context)


@router.get("/{pk}/destruction")
async def destruction_key_document_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
    key = await KeyDocumentServise.get_by_id(pk)
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
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
            ["get_key_documents_admin", "destruction_key_document_admin"],
        ),
        "user": user
    }
    return templates.TemplateResponse(destruction_tepmlate, context)


@router.post("/{pk}/destruction")
async def destruct_key_document_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
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

            return redirect(
                request=request,
                endpoint="get_key_documents_admin",
                msg="Ключевой документ выведен из эксплуатации!"
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
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
            ["get_key_documents_admin", "decommissioning_cversion_admin"],
        ),
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(destruction_tepmlate, context)


@router.get("/{pk}/c_destruction")
async def destruct_employee_cversion_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
    key = await KeyDocumentServise.get_by_id(pk)
    responsible_user_cryptography_keys, _ = await KeyDocumentServise.all(
        filters={
            "owner_id": key.owner_id,
            "cryptography_version_id": key.cryptography_version_id,
            "remove_act_record_id": None,
        }
    )
    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
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
            ["get_key_documents_admin", "destruct_employee_cversion_admin"],
        ),
        "user": user
    }
    return templates.TemplateResponse(c_destruction_tepmlate, context)


@router.post("/{pk}/c_destruction")
async def destruct_key_cversion_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
    key = await KeyDocumentServise.get_by_id(pk)
    user_cryptography_keys, _ = await KeyDocumentServise.all(
        filters={
            "owner_id": key.owner_id,
            "cryptography_version_id": key.cryptography_version_id,
            "remove_act_record_id": None,
            "user": user
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
                action_date=action_date,
            )

            return redirect(
                request=request,
                endpoint="get_key_documents_admin",
                msg="СКЗИ выведено из эксплуатации!"
            )
        except Exception as e:
            print("-------------------------------")
            print(e)
            print("-------------------------------")
            form.errors.setdefault("non_field_error", e)

    security_staff_members = await EmployeeServise.get_short_list(is_staff=True)
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
            ["get_key_documents_admin", "decommissioning_cversion_admin"],
        ),
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(c_destruction_tepmlate, context)


@router.get("/{pk}/edit")
async def edit_key_document_admin(pk: int, request: Request):
    pass
