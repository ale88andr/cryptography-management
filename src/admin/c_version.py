from typing import Any, Dict, Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_CVERSION_ADD_HEADER as add_header,
    ADMIN_CVERSION_EDIT_HEADER as edit_header,
    ADMIN_CVERSION_DESCRIPTION as help_text,
    ADMIN_CVERSION_INDEX_HEADER as index_header,
    ADMIN_CVERSION_DECOMIS_HEADER as decommissioning_header,
    ADMIN_CVERSION as app_prefix,
    ADMIN_CVERSION_FORM_TPL as form_template,
    ADMIN_CVERSION_LIST_TPL as list_template,
    ADMIN_CVERSION_DECOMIS_TPL as decommissioning_form_template,
)
from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    redirect_with_message,
)
from dependencies.auth import get_current_admin
from forms.c_version import CVersionForm
from forms.c_version_decommissioning import CVersionDecommissioningForm
from services.c_version import CVersionServise
from services.c_model import CModelServise
from services.c_logbook import CLogbookServise
from services.employee import EmployeeServise
from services.c_grade import CryptographyGradeServise
from models.users import User
from core.exceptions import LogbookOnDeleteException
from utils.formatting import format_date, format_string


router = APIRouter(prefix=app_prefix, tags=[help_text])


# Создание фильтров сотрудников для методов: get_employees_admin, get_cusers_admin
def create_filters(
    filter_model_id: Optional[int] = None,
    filter_grade_id: Optional[int] = None,
) -> Dict[str, Any]:
    return {
        key: value
        for key, value in {
            "model_id": filter_model_id,
            "grade_id": filter_grade_id,
        }.items()
        if value is not None and value > 0
    }


# ========= Cryptography Models Versions =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cversions_admin(
    request: Request,
    msg: str = None,
    error: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_model_id: Optional[int] = None,
    filter_grade_id: Optional[int] = None,
    user: User = Depends(get_current_admin),
):
    filters = create_filters(filter_model_id, filter_grade_id)

    records, counter = await CVersionServise.all(sort=sort, q=q, filters=filters)
    models, _ = await CModelServise.all()
    cryptography_grades = await CryptographyGradeServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update({
        "versions": records,
        "counter": counter,
        "grades": cryptography_grades,
        "models": models,
        "filter_model_id": filter_model_id,
        "filter_grade_id": filter_grade_id,
        "msg": msg,
        "error": error,
        "sort": sort,
        "q": q,
        "breadcrumbs": create_breadcrumbs(
            router, [index_header], ["get_cversions_admin"]
        ),
    })
    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_cversion_admin(request: Request, user: User = Depends(get_current_admin)):
    models, _ = await CModelServise.all()
    responsible_users = await EmployeeServise.get_short_list(is_staff=True)
    cryptography_grades = await CryptographyGradeServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update({
        "grades": cryptography_grades,
        "models": models,
        "model_id": None,
        "is_created": True,
        "responsible_user_id": None,
        "responsible_users": responsible_users,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, add_header],
            ["get_cversions_admin", "add_cversion_admin"],
        ),
    })

    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_cversion_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = CVersionForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            await CVersionServise.register(
                version=format_string(form.version),
                model_id=int(form.model_id),
                # grade=CryptographyGrade(int(form.grade)),
                grade_id=int(form.grade_id),
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
            return redirect_with_message(
                request,
                "get_cversions_admin",
                msg=f"Версия СКЗИ зарегистрирована!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    models, _ = await CModelServise.all()
    responsible_users = await EmployeeServise.get_short_list(is_staff=True)
    cryptography_grades = await CryptographyGradeServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update({
        "grades": cryptography_grades,
        "models": models,
        "is_created": True,
        "responsible_user_id": None,
        "responsible_users": responsible_users,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, add_header],
            ["get_cversions_admin", "add_cversion_admin"],
        ),
    })
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/edit")
async def edit_cversion_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    obj = await CVersionServise.get_by_id(pk)
    responsible_users = await EmployeeServise.get_short_list(is_staff=True)
    models, _ = await CModelServise.all()
    cryptography_grades = await CryptographyGradeServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update({
        "grades": cryptography_grades,
        "models": models,
        "responsible_users": responsible_users,
        "happened_at": obj.install_act.action_date,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, edit_header],
            ["get_cversions_admin", "edit_cversion_admin"],
        ),
    })
    context.update(obj.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.post("/{pk}/edit")
async def update_cversion_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    form = CVersionForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CVersionServise.update(
                pk,
                version=format_string(form.version),
                grade_id=int(form.grade_id),
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
            return redirect_with_message(
                request,
                "get_cversions_admin",
                msg=f"Версия СКЗИ '{obj.version}' обновлена!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    models, _ = await CModelServise.all()
    responsible_users = await EmployeeServise.get_short_list(is_staff=True)
    cryptography_grades = await CryptographyGradeServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update({
        "grades": cryptography_grades,
        "models": models,
        "responsible_users": responsible_users,
        "id": pk,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, edit_header],
            ["get_cversions_admin", "edit_cversion_admin"],
        ),
    })
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/decommissioning")
async def decommissioning_cversion_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    performers = await EmployeeServise.get_short_list(is_staff=True)

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, decommissioning_header, help_text, user
    )
    context.update({
        "performers": performers,
        "head_commision_member_id": None,
        "commision_member_id": None,
        "performer_id": None,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, decommissioning_header],
            ["get_cversions_admin", "decommissioning_cversion_admin"],
        ),
    })
    return templates.TemplateResponse(decommissioning_form_template, context)


@router.post("/{pk}/decommissioning")
async def set_decommissioning_cversion_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    version = await CVersionServise.get_by_id(pk)
    form = CVersionDecommissioningForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid() and not version.remove_act_record_id:
        try:
            await CVersionServise.unregister(
                version_id=pk,
                head_commision_member_id=int(form.head_commision_member_id),
                commision_member_id=int(form.commision_member_id),
                performer_id=int(form.performer_id),
                reason=format_string(form.reason),
                action_date=format_date(form.action_date),
            )
            return redirect_with_message(
                request,
                "get_cversions_admin",
                msg=f"Экземпляр СКЗИ выведен из эксплуатации!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    performers = await EmployeeServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, decommissioning_header, help_text, user
    )
    context.update({
        "performers": performers,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, decommissioning_header],
            ["get_cversions_admin", "decommissioning_cversion_admin"],
        ),
    })
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(decommissioning_form_template, context)


@router.get("/{pk}/delete")
async def delete_cversion_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    redirect_url = request.url_for("get_cversions_admin")
    redirect_code = status.HTTP_303_SEE_OTHER
    try:
        log = await CLogbookServise.get_one_or_none(cryptography_version_id=pk)
        if log:
            raise LogbookOnDeleteException
        await CVersionServise.delete(pk)
        redirect_url = redirect_url.include_query_params(msg="Версия СКЗИ удалена!")
    except Exception as e:
        redirect_url = redirect_url.include_query_params(error=e)

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)
