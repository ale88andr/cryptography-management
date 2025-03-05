from typing import Dict, Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_CARRIER_ADD_HEADER as add_header,
    ADMIN_CARRIER_EDIT_HEADER as edit_header,
    ADMIN_CARRIER_DESCRIPTION as help_text,
    ADMIN_CARRIER_INDEX_HEADER as index_header,
    ADMIN_CARRIER as app_prefix,
    ADMIN_CARRIER_FORM_TPL as form_template,
    ADMIN_CARRIER_LIST_TPL as list_template,
)
from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    redirect_with_error,
    redirect_with_message,
)
from dependencies.auth import get_current_admin
from forms.key_carrier import KeyCarrierForm
from models.users import User
from services.key_carrier import KeyCarrierServise
from services.carrier_types import CarrierTypesServise
from services.key_document import KeyDocumentServise


router = APIRouter(prefix=app_prefix, tags=[help_text])
index_url = "get_carriers_admin"


def create_filters(filter_type_id: Optional[int]) -> Dict[str, int]:
    filters = {}
    if filter_type_id and filter_type_id > 0:
        filters["carrier_type_id"] = filter_type_id
    return filters


# ========= Carriers =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_carriers_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_type_id: Optional[int] = None,
    error: Optional[str] = None,
    user: User = Depends(get_current_admin),
):
    filters = create_filters(filter_type_id)

    records, counter = await KeyCarrierServise.get_list(sort=sort, q=q, filters=filters)
    carrier_types, _ = await CarrierTypesServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "objects": records,
            "counter": counter,
            "carrier_types": carrier_types,
            "filter_type_id": filter_type_id,
            "msg": msg,
            "error": error,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_header], [index_url]
            ),
        }
    )
    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_carrier_admin(request: Request, user: User = Depends(get_current_admin)):
    carrier_types, _ = await CarrierTypesServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "carrier_types": carrier_types,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                [index_url, "add_carrier_admin"],
            ),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_carrier_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = KeyCarrierForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await KeyCarrierServise.add(
                serial=form.serial, carrier_type_id=int(form.type_id)
            )
            return redirect_with_message(
                request,
                index_url,
                msg=f"Ключевой носитель '{obj.serial}' создан!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    carrier_types, _ = await CarrierTypesServise.all()
    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "carrier_types": carrier_types,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                [index_url, "add_carrier_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{carrier_id}/edit")
async def edit_carrier_admin(
    carrier_id: int, request: Request, user: User = Depends(get_current_admin)
):
    obj = await KeyCarrierServise.get_by_id(carrier_id)
    carrier_types, _ = await CarrierTypesServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "carrier_types": carrier_types,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                [index_url, "edit_carrier_admin"],
            ),
            **vars(obj),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/{carrier_id}/edit")
async def update_carrier_admin(
    carrier_id: int, request: Request, user: User = Depends(get_current_admin)
):
    form = KeyCarrierForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await KeyCarrierServise.update(carrier_id, name=form.name)
            return redirect_with_message(
                request,
                index_url,
                msg=f"Тип ключевого носителя '{obj.name}' обновлен!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                [index_url, "edit_carrier_admin"],
            )
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_carrier_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    carrier = await KeyCarrierServise.get_by_id(pk)

    if not carrier:
        return redirect_with_error(request, index_url, "Ключевой носитель не найден.")

    keys = await KeyDocumentServise.all(carrier_id=carrier.id)

    if keys:
        key_names = "; ".join([item.serial for item in keys])
        return redirect_with_error(
            request,
            index_url,
            f"Невозможно удалить ключевой носитель '{carrier.serial}', так как от неё зависит ключевая информация: {key_names}, которая была учтена ранее!"
        )

    try:
        await KeyCarrierServise.delete(pk)
        return redirect_with_message(request, index_url, "Ключевой носитель удален!")
    except Exception as e:
        return redirect_with_error(
            request,
            index_url,
            f"Необработанная ошибка удаления ключевого носителя '{carrier.serial}': {e}"
        )
