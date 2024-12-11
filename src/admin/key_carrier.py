from typing import Dict, Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    CARRIERS_ADD_PAGE_HEADER as add_header,
    CARRIERS_EDIT_PAGE_HEADER as edit_header,
    CARRIERS_HELP_TEXT as help_text,
    CARRIERS_INDEX_PAGE_HEADER as index_header,
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

app_prefix = "/admin/cryptography/carriers"
form_template = f"{app_prefix}/form.html"
list_template = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[help_text])


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
    user: User = Depends(get_current_admin),
):
    filters = create_filters(filter_type_id)

    records, counter = await KeyCarrierServise.all(sort=sort, q=q, filters=filters)
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
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_header], ["get_carriers_admin"]
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
                ["get_carriers_admin", "add_carrier_admin"],
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
                "get_carriers_admin",
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
                ["get_carriers_admin", "add_carrier_admin"],
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
                ["get_carriers_admin", "edit_carrier_admin"],
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
                "get_carriers_admin",
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
                ["get_carriers_admin", "edit_carrier_admin"],
            )
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{carrier_id}/delete")
async def delete_carrier_admin(
    carrier_id: int, request: Request, user: User = Depends(get_current_admin)
):
    try:
        await KeyCarrierServise.delete(carrier_id)
        return redirect_with_message(
            request, "get_carriers_admin", msg="Ключевой носитель удален!"
        )
    except Exception as e:
        return redirect_with_error(
            request, "get_carriers_admin", errors={"non_field_error": str(e)}
        )
