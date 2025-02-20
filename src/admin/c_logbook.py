from dataclasses import asdict

from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_CLOG_DESCRIPTION as hepl_text,
    ADMIN_CLOG_INDEX_HEADER as index_page_header,
    ADMIN_CLOG as app_prefix,
    ADMIN_CLOG_FORM_TPL as form_teplate,
    ADMIN_CLOG_LIST_TPL as list_template,
)
from core.config import templates
from core.utils import create_breadcrumbs, create_file_response
from dependencies.auth import get_current_admin
from models.users import User

from services.c_logbook import CLogbookServise
from core.templater import (
    DocumentTemplatesEnum,
    InstallVersionActDocumentContext,
    LogbookTemplatesEnum,
    UninstallVersionActDocumentContext,
)
from services.c_version import CVersionServise
from utils.formatting import get_str_now_date, format_date_to_str, get_date_tuple


router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Cryptography Models Versions =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_clogbook_admin(
    request: Request,
    msg: str = None,
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

    records, counter = await CLogbookServise.all(sort=sort)
    context = {
        "request": request,
        "objects": records,
        "counter": counter,
        "page_header": index_page_header,
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
    return templates.TemplateResponse(list_template, context)


@router.get("/{record_id}/delete")
async def delete_clogbook_admin(record_id: int, request: Request, user: User = Depends(get_current_admin)):
    redirect_url = request.url_for("get_clogbook_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await CLogbookServise.delete(record_id)
        redirect_url = redirect_url.include_query_params(msg="Запись журнала удалена!")
    except Exception as e:
        redirect_url = redirect_url.include_query_params(errors={"non_field_error": e})

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)


@router.get("/{record_id}/install/doc")
async def download_creation_act_admin(record_id: int, request: Request, user: User = Depends(get_current_admin)):
    cryptography = await CVersionServise.get_by_id(record_id)
    _, month, year = get_date_tuple(cryptography.install_act.action_date)

    context = InstallVersionActDocumentContext(
        action_date=format_date_to_str(cryptography.install_act.action_date),
        number=cryptography.install_act.number,
        month=month,
        year=year,
        reason_num=cryptography.received_num,
        reason_date=format_date_to_str(cryptography.received_at),
        performer=cryptography.responsible_user.short_name,
        performer_position=cryptography.responsible_user.full_position,
        cryptography_version=str(cryptography),
        cryptography_version_set="\n".join(cryptography.doc_set),
        sender=cryptography.received_from,
    )

    return create_file_response(
        DocumentTemplatesEnum.C_INSTALL.value,
        asdict(context),
        cryptography.install_act.number,
    )


@router.get("/{record_id}/remove/doc")
async def download_decommissioning_act_admin(record_id: int, request: Request, user: User = Depends(get_current_admin)):
    cryptography = await CVersionServise.get_by_id(record_id)
    _, month, year = get_date_tuple(cryptography.remove_act.action_date)

    context = UninstallVersionActDocumentContext(
        action_date=format_date_to_str(cryptography.remove_act.action_date),
        number=cryptography.remove_act.number,
        month=month,
        year=year,
        performer=cryptography.remove_act.performer.short_name,
        performer_position=cryptography.remove_act.performer.full_position,
        cryptography_version=str(cryptography),
        cryptography_version_set="\n".join(cryptography.doc_set),
        sender=cryptography.received_from,
        reason=cryptography.remove_act.reason,
        head_commision_member=cryptography.remove_act.head_commision_member.short_name,
        head_commision_member_position=cryptography.remove_act.head_commision_member.full_position,
        commision_member=cryptography.remove_act.commision_member.short_name,
        commision_member_position=cryptography.remove_act.commision_member.full_position,
    )

    return create_file_response(
        DocumentTemplatesEnum.C_REMOVE.value,
        asdict(context),
        cryptography.install_act.number,
    )


@router.get("/doc")
async def download_clogbook_admin(request: Request, user: User = Depends(get_current_admin)):
    objects, _ = await CLogbookServise.all()

    return create_file_response(
        LogbookTemplatesEnum.LOGBOOK.value,
        {"objects": objects},
        f"Журнал учета СКЗИ на дату - {get_str_now_date()}",
    )
