from typing import Optional
from fastapi import APIRouter, Request, Depends

from admin.constants import (
    ADMIN_BUILD_DESCRIPTION,
    ADMIN_BUILD_INDEX_HEADER,
    ADMIN_BUILD_ADD_HEADER,
    ADMIN_BUILD_EDIT_HEADER,
    ADMIN_BUILD as app_prefix,
    ADMIN_BUILD_FORM_TPL as form_template,
    ADMIN_BUILD_LIST_TPL as list_template,
)
from core.config import templates
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    redirect,
    redirect_with_error,
    redirect_with_message
)
from dependencies.auth import get_current_admin
from forms.building import BuildingForm
from models.users import User
from services.building import BuildingServise
from services.location import LocationServise


router = APIRouter(prefix=app_prefix, tags=[ADMIN_BUILD_DESCRIPTION])
index_url = "get_buildings_admin"


# ========= Buildings =========
@router.get("/")
async def get_buildings_admin(
    request: Request, msg: Optional[str] = None, error: Optional[str] = None, user: User = Depends(get_current_admin)
):
    records = await BuildingServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_BUILD_INDEX_HEADER, ADMIN_BUILD_DESCRIPTION, user
    )
    context.update(
        {
            "buildings": records,
            "counter": len(records),
            "msg": msg,
            "error": error,
            "breadcrumbs": create_breadcrumbs(
                router, [ADMIN_BUILD_INDEX_HEADER], [index_url]
            ),
        }
    )

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_building_admin(request: Request, user: User = Depends(get_current_admin)):
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_BUILD_ADD_HEADER, ADMIN_BUILD_DESCRIPTION, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [ADMIN_BUILD_INDEX_HEADER, ADMIN_BUILD_ADD_HEADER],
                [index_url, "add_buildings_admin"],
            ),
        }
    )
    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_building_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = BuildingForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            building = await BuildingServise.add(
                name=form.name,
                city=form.city,
                street=form.street,
                building=form.building,
                index=int(form.index) if form.index else None,
            )

            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Филиал '{building.name}' добавлен!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_BUILD_ADD_HEADER, ADMIN_BUILD_DESCRIPTION, user
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{building_id}/edit")
async def edit_building_admin(
    building_id: int, request: Request, user: User = Depends(get_current_admin)
):
    building = await BuildingServise.get_one_or_none(id=building_id)
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_BUILD_EDIT_HEADER, ADMIN_BUILD_DESCRIPTION, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [ADMIN_BUILD_INDEX_HEADER, ADMIN_BUILD_EDIT_HEADER],
                [index_url, "edit_buildings_admin"],
            ),
            **vars(building),
        }
    )

    return templates.TemplateResponse(form_template, context)


@router.post("/{building_id}/edit")
async def update_building_admin(
    building_id: int, request: Request, user: User = Depends(get_current_admin)
):
    form = BuildingForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            building = await BuildingServise.update(
                model_id=building_id,
                name=form.name,
                city=form.city,
                street=form.street,
                building=form.building,
                index=int(form.index) if form.index else None,
            )

            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Данные '{building.name}' успешно обновлены!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, ADMIN_BUILD_EDIT_HEADER, ADMIN_BUILD_DESCRIPTION, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [ADMIN_BUILD_INDEX_HEADER, ADMIN_BUILD_EDIT_HEADER],
                [index_url, "edit_buildings_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_building_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    building = await BuildingServise.get_by_id(pk)

    if not building:
        return redirect_with_error(request, index_url, "Филиал не найден.")

    locations = await LocationServise.all(building_id=building.id)

    if locations:
        location_names = ", ".join([item.name for item in locations])
        return redirect_with_error(
            request,
            index_url,
            f"Невозможно удалить филиал '{building}', так как он связан с рабочими местами: {location_names}"
        )

    if building:
        try:
            await BuildingServise.delete(pk)
            return redirect_with_message(request, index_url, "Филиал удален!")
        except Exception as e:
            return redirect_with_error(
                request,
                index_url,
                f"Необработанная ошибка удаления филиала '{building}': {e}"
            )
