from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    VER_ADD_PAGE_HEADER as add_page_header,
    VER_EDIT_PAGE_HEADER as edit_page_header,
    VER_HELP_TEXT as hepl_text,
    VER_INDEX_PAGE_HEADER as index_page_header,
    VER_DECOMMISSIONING_TEXT as decommissioning_page_header,
)
from core.config import templates
from core.utils import create_breadcrumbs
from dependencies.auth import get_current_admin
from forms.c_version import CVersionForm
from forms.c_version_decommissioning import CVersionDecommissioningForm
from services.c_version import CVersionServise
from services.c_model import CModelServise
from services.c_logbook import CLogbookServise
from services.employee import EmployeeServise
from models.cryptography import CPRODUCT_GRADES, CryptographyGrade
from models.users import User
from core.exceptions import LogbookOnDeleteException
from utils.formatting import format_date, format_string

app_prefix = "/admin/cryptography/versions"
form_teplate = f"{app_prefix}/form.html"
decommissioning_form_template = f"{app_prefix}/decommissioning.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Cryptography Models Versions =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cversions_admin(
    request: Request,
    msg: str = None,
    error: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_model_id: Optional[int] = None,
    filter_grade: Optional[int] = None,
    user: User = Depends(get_current_admin)
):
    filters = {}

    if filter_model_id and filter_model_id > 0:
        filters["model_id"] = filter_model_id

    if filter_grade:
        filters["grade"] = filter_grade

    records, counter = await CVersionServise.all(sort=sort, q=q, filters=filters)
    models, _ = await CModelServise.all()
    context = {
        "request": request,
        "versions": records,
        "counter": counter,
        "page_header": index_page_header,
        "page_header_help": hepl_text,
        "grades": CPRODUCT_GRADES,
        "models": models,
        "filter_model_id": filter_model_id,
        "filter_grade": filter_grade,
        "msg": msg,
        "error": error,
        "sort": sort,
        "q": q,
        "breadcrumbs": create_breadcrumbs(
            router, [index_page_header], ["get_cversions_admin"]
        ),
        "user": user,
    }
    return templates.TemplateResponse(list_teplate, context)


@router.get("/add")
async def add_cversion_admin(request: Request, user: User = Depends(get_current_admin)):
    models, _ = await CModelServise.all()
    responsible_users = await EmployeeServise.get_all_shortened(is_staff=True)
    context = {
        "request": request,
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "models": models,
        "model_id": None,
        "is_created": True,
        "responsible_user_id": None,
        "responsible_users": responsible_users,
        "grades": CPRODUCT_GRADES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_cversions_admin", "add_cversion_admin"],
        ),
        "user": user,
    }
    return templates.TemplateResponse(form_teplate, context)


@router.post("/add")
async def create_cversion_admin(request: Request, user: User = Depends(get_current_admin)):
    form = CVersionForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            await CVersionServise.register(
                version=format_string(form.version),
                model_id=int(form.model_id),
                grade=CryptographyGrade(int(form.grade)),
                serial=format_string(form.serial),
                dist_num=format_string(form.dist_num),
                certificate=format_string(form.certificate),
                certificate_expired_at=format_date(form.certificate_expired_at),
                received_num=format_string(form.received_num),
                received_from=format_string(form.received_from),
                received_at=format_date(form.received_at),
                form=format_string(form.form),
                license=format_string(form.license),
                responsible_user_id=int(form.responsible_user_id),
                comment=format_string(form.comment),
                action_date=format_date(form.happened_at),
            )

            return responses.RedirectResponse(
                request.url_for("get_cversions_admin").include_query_params(
                    msg="Версия СКЗИ зарегистрирована!"
                ),
                status_code=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    models, _ = await CModelServise.all()
    responsible_users = await EmployeeServise.get_all_shortened(is_staff=True)
    context = {
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "models": models,
        "responsible_users": responsible_users,
        "is_created": True,
        "grades": CPRODUCT_GRADES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_cversions_admin", "add_cversion_admin"],
        ),
        "user": user,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{cversion_id}/edit")
async def edit_cversion_admin(cversion_id: int, request: Request, user: User = Depends(get_current_admin)):
    obj = await CVersionServise.get_by_id(cversion_id)
    responsible_users = await EmployeeServise.get_all_shortened(is_staff=True)
    models, _ = await CModelServise.all()
    context = {
        "request": request,
        "page_header": edit_page_header,
        "page_header_help": hepl_text,
        "responsible_users": responsible_users,
        "happened_at": obj.install_act.action_date,
        "models": models,
        "grades": CPRODUCT_GRADES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, edit_page_header],
            ["get_cversions_admin", "add_cversion_admin"],
        ),
        "user": user,
    }
    context.update(obj.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.post("/{cversion_id}/edit")
async def update_cversion_admin(cversion_id: int, request: Request, user: User = Depends(get_current_admin)):
    form = CVersionForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CVersionServise.update(
                cversion_id,
                version=format_string(form.version),
                grade=CryptographyGrade(int(form.grade)),
                serial=format_string(form.serial),
                dist_num=format_string(form.dist_num),
                certificate=format_string(form.certificate),
                certificate_expired_at=format_date(form.certificate_expired_at),
                received_num=format_string(form.received_num),
                received_from=format_string(form.received_from),
                received_at=format_date(form.received_at),
                form=format_string(form.form),
                license=format_string(form.license),
                comment=format_string(form.comment),
            )
            redirect_url = request.url_for("get_cversions_admin").include_query_params(
                msg=f"Версия СКЗИ '{obj.version}' обновлена!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    models, _ = await CModelServise.all()
    responsible_users = await EmployeeServise.get_all_shortened(is_staff=True)
    context = {
        "request": request,
        "id": cversion_id,
        "page_header": edit_page_header,
        "page_header_help": hepl_text,
        "responsible_users": responsible_users,
        "models": models,
        "grades": CPRODUCT_GRADES,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, edit_page_header],
            ["get_cversions_admin", "add_cversion_admin"],
        ),
        "user": user,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{cversion_id}/decommissioning")
async def decommissioning_cversion_admin(cversion_id: int, request: Request, user: User = Depends(get_current_admin)):
    performers = await EmployeeServise.get_all_shortened(is_staff=True)
    context = {
        "request": request,
        "page_header": decommissioning_page_header,
        "page_header_help": hepl_text,
        "performers": performers,
        "head_commision_member_id": None,
        "commision_member_id": None,
        "performer_id": None,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, decommissioning_page_header],
            ["get_cversions_admin", "decommissioning_cversion_admin"],
        ),
        "user": user,
    }
    return templates.TemplateResponse(decommissioning_form_template, context)


@router.post("/{cversion_id}/decommissioning")
async def set_decommissioning_cversion_admin(cversion_id: int, request: Request, user: User = Depends(get_current_admin)):
    version = await CVersionServise.get_by_id(cversion_id)
    form = CVersionDecommissioningForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid() and not version.remove_act_record_id:
        try:
            await CVersionServise.unregister(
                version_id=cversion_id,
                head_commision_member_id=int(form.head_commision_member_id),
                commision_member_id=int(form.commision_member_id),
                performer_id=int(form.performer_id),
                reason=format_string(form.reason),
                action_date=format_date(form.action_date),
            )

            redirect_url = request.url_for("get_cversions_admin").include_query_params(
                msg=f"Экземпляр СКЗИ выведен из эксплуатации!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    performers = await EmployeeServise.all()
    context = {
        "request": request,
        "page_header": decommissioning_page_header,
        "page_header_help": hepl_text,
        "performers": performers,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, decommissioning_page_header],
            ["get_cversions_admin", "decommissioning_cversion_admin"],
        ),
        "user": user,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(decommissioning_form_template, context)


@router.get("/{cversion_id}/delete")
async def delete_cversion_admin(cversion_id: int, request: Request, user: User = Depends(get_current_admin)):
    redirect_url = request.url_for("get_cversions_admin")
    redirect_code = status.HTTP_303_SEE_OTHER
    try:
        log = await CLogbookServise.get_one_or_none(cryptography_version_id=cversion_id)
        if log:
            raise LogbookOnDeleteException
        await CVersionServise.delete(cversion_id)
        redirect_url = redirect_url.include_query_params(msg="Версия СКЗИ удалена!")
    except Exception as e:
        redirect_url = redirect_url.include_query_params(error=e)

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)
