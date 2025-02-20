from typing import Dict, Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_LOCATION_ADD_HEADER as add_header,
    ADMIN_LOCATION_EDIT_HEADER as edit_header,
    ADMIN_LOCATION_INDEX_HEADER as index_header,
    ADMIN_LOCATION_DESCRIPTION as help_text,
    ADMIN_LOCATION as app_prefix,
    ADMIN_LOCATION_LIST_TPL as list_template,
    ADMIN_LOCATION_FORM_TPL as form_template,
)
from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    redirect_with_error,
    redirect_with_message,
)
from dependencies.auth import get_current_admin
from forms.locations import LocationForm
from models.users import User
from services.building import BuildingServise
from services.location import LocationServise


router = APIRouter(prefix=app_prefix, tags=[help_text])


def create_filters(filter_building_id: Optional[int]) -> Dict[str, int]:
    filters = {}
    if filter_building_id and filter_building_id > 0:
        filters["building_id"] = filter_building_id
    return filters


# ========= Locations =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_locations_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_building_id: Optional[int] = None,
    user: User = Depends(get_current_admin),
):
    filters = create_filters(filter_building_id)

    records, counter = await LocationServise.all(sort=sort, q=q, filters=filters)

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update(
        {
            "locations": records,
            "counter": counter,
            "buildings": await BuildingServise.all(),
            "filter_building_id": filter_building_id,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_header], ["get_locations_admin"]
            ),
        }
    )

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_location_admin(request: Request, user: User = Depends(get_current_admin)):
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(
        {
            "buildings": await BuildingServise.all(),
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, add_header],
                ["get_locations_admin", "add_location_admin"],
            ),
        }
    )
    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_loc_admin(request: Request, user: User = Depends(get_current_admin)):
    form = LocationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            loc = await LocationServise.add(
                name=form.name, building_id=int(form.building_id)
            )
            return redirect_with_message(
                request,
                "get_locations_admin",
                msg=f"Рабочее место '{loc.name}' создано!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update(form.__dict__)
    context.update(form.fields)
    context.update({"buildings": await BuildingServise.all()})
    return templates.TemplateResponse(form_template, context)


@router.get("/{location_id}/edit")
async def edit_location_admin(
    location_id: int, request: Request, user: User = Depends(get_current_admin)
):
    loc = await LocationServise.get_by_id(location_id)

    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_locations_admin", "edit_locations_admin"],
            ),
            "buildings": await BuildingServise.all(),
            **vars(loc),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/{location_id}/edit")
async def update_location_admin(
    location_id: int, request: Request, user: User = Depends(get_current_admin)
):
    form = LocationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            loc = await LocationServise.update(
                location_id, name=form.name, building_id=int(form.building_id)
            )
            return redirect_with_message(
                request,
                "get_locations_admin",
                msg=f"Рабочее место '{loc.name}' обновлено!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_header, edit_header],
                ["get_locations_admin", "edit_locations_admin"],
            ),
            "buildings": await BuildingServise.all(),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{location_id}/delete")
async def delete_location_admin(
    location_id: int, request: Request, user: User = Depends(get_current_admin)
):
    try:
        await LocationServise.delete(location_id)
        return redirect_with_message(
            request, "get_locations_admin", msg="Рабочее место удалено!"
        )
    except Exception as e:
        return redirect_with_error(
            request, "get_locations_admin", errors={"non_field_error": str(e)}
        )
