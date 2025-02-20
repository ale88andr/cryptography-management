from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_CMANUFACTURER_ADD_HEADER as add_header,
    ADMIN_CMANUFACTURER_EDIT_HEADER as edit_header,
    ADMIN_CMANUFACTURER_DESCRIPTION as help_text,
    ADMIN_CMANUFACTURER_INDEX_HEADER as index_header,
    ADMIN_CMANUFACTURER as app_prefix,
    ADMIN_CMANUFACTURER_LIST_TPL as form_template,
    ADMIN_CMANUFACTURER_FORM_TPL as list_template,
)
from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    redirect_with_error,
    redirect_with_message,
)
from dependencies.auth import get_current_admin
from forms.cryptography_manufacturer import CryptographyManufacturerForm
from services.c_manufacturer import CManufacturerServise
from models.users import User


router = APIRouter(prefix=app_prefix, tags=[help_text])


# ========= Cryptography Manufacturers =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cmanufacturers_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    user: User = Depends(get_current_admin),
):
    records, counter = await CManufacturerServise.all(sort=sort, q=q)

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "objects": records,
            "counter": counter,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_header], ["get_cmanufacturers_admin"]
            ),
        }
    )

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_cmanufacturer_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                ["get_cmanufacturers_admin", "add_cmanufacturer_admin"],
            ),
        }
    )
    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_cmanufacturer_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = CryptographyManufacturerForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CManufacturerServise.add(name=form.name)
            return redirect_with_message(
                request,
                "get_cmanufacturers_admin",
                msg=f"Производитель СКЗИ '{obj.name}' создан!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                ["get_cmanufacturers_admin", "add_cmanufacturer_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/edit")
async def edit_cmanufacturer_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    manufacturer = await CManufacturerServise.get_by_id(pk)

    # Создаем базовый контекст
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_cmanufacturers_admin", "edit_cmanufacturer_admin"],
            ),
            **vars(manufacturer),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/{pk}/edit")
async def update_carrier_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    form = CryptographyManufacturerForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CManufacturerServise.update(pk, name=form.name)
            return redirect_with_message(
                request,
                "get_cmanufacturers_admin",
                msg=f"Тип ключевого носителя '{obj.name}' обновлен!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_cmanufacturers_admin", "edit_cmanufacturer_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_cmanufacturer_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    try:
        await CManufacturerServise.delete(pk)
        return redirect_with_message(
            request, "get_cmanufacturers_admin", msg="Отдел удален!"
        )
    except Exception as e:
        return redirect_with_error(
            request, "get_cmanufacturers_admin", errors={"non_field_error": str(e)}
        )
