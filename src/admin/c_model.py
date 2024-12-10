from typing import Dict, Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    CMODEL_ADD_PAGE_HEADER as add_header,
    CMODEL_EDIT_PAGE_HEADER as edit_header,
    CMODEL_HELP_TEXT as help_text,
    CMODEL_INDEX_PAGE_HEADER as index_header,
)
from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    redirect_with_error,
    redirect_with_message,
)
from dependencies.auth import get_current_admin
from forms.c_model import CModelForm
from services.c_model import CModelServise
from services.c_manufacturer import CManufacturerServise
from models.cryptography import CRYPTO_MODEL_TYPES, ModelTypes
from models.users import User


app_prefix = "/admin/cryptography/models"
form_template = f"{app_prefix}/form.html"
list_template = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[help_text])


def create_filters(
    filter_manufacturer_id: Optional[int], filter_type: Optional[int]
) -> Dict[str, int]:
    filters = {}
    if filter_manufacturer_id and filter_manufacturer_id > 0:
        filters["manufacturer_id"] = filter_manufacturer_id
    if filter_type:
        filters["type"] = ModelTypes(filter_type)
    return filters


# ========= Cryptography Models =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_cmodels_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_manufacturer_id: Optional[int] = None,
    filter_type: Optional[int] = None,
    user: User = Depends(get_current_admin),
):
    filters = create_filters(filter_manufacturer_id, filter_type)

    records, counter = await CModelServise.all(sort=sort, q=q, filters=filters)
    manufacturers, _ = await CManufacturerServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "objects": records,
            "counter": counter,
            "manufacturers": manufacturers,
            "filter_manufacturer_id": filter_manufacturer_id,
            "filter_type": filter_type,
            "types": CRYPTO_MODEL_TYPES,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_header], ["get_cmodels_admin"]
            ),
        }
    )
    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_cmodel_admin(request: Request, user: User = Depends(get_current_admin)):
    manufacturers, _ = await CManufacturerServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(
        {
            "manufacturers": manufacturers,
            "manufacturer_id": None,
            "type": None,
            "types": CRYPTO_MODEL_TYPES,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                ["get_cmodels_admin", "add_cmodel_admin"],
            ),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_cmodel_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = CModelForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CModelServise.add(
                name=form.name,
                manufacturer_id=int(form.manufacturer_id),
                type=int(form.type),
                description=form.description,
            )
            return redirect_with_message(
                request,
                "get_cmodels_admin",
                msg=f"Модель СКЗИ '{obj.name}' создана!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    manufacturers, _ = await CManufacturerServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(
        {
            "manufacturers": manufacturers,
            "manufacturer_id": None,
            "type": None,
            "types": CRYPTO_MODEL_TYPES,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                ["get_cmodels_admin", "add_cmodel_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/edit")
async def edit_cmodel_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    obj = await CModelServise.get_by_id(pk)
    manufacturers, _ = await CManufacturerServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "manufacturers": manufacturers,
            "types": CRYPTO_MODEL_TYPES,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_cmodels_admin", "edit_cmodel_admin"],
            ),
            **vars(obj),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/{pk}/edit")
async def update_cmodel_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    form = CModelForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            await CModelServise.update(
                pk,
                name=form.name,
                manufacturer_id=int(form.manufacturer_id),
                type=ModelTypes(int(form.type)),
                description=form.description,
            )
            return redirect_with_message(
                request,
                "get_cmodels_admin",
                msg=f"Модель СКЗИ обновлена!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    manufacturers, _ = await CManufacturerServise.all()
    # Создаем базовый контекст
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "manufacturers": manufacturers,
            "types": CRYPTO_MODEL_TYPES,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_cmodels_admin", "edit_cmodel_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_cmodel_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    try:
        await CModelServise.delete(pk)
        return redirect_with_message(
            request, "get_cmodels_admin", msg="Модель СКЗИ удалена!"
        )
    except Exception as e:
        return redirect_with_error(
            request, "get_cmodels_admin", errors={"non_field_error": str(e)}
        )
