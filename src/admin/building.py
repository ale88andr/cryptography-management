from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    BUILD_ADD_PAGE_HEADER,
    BUILD_EDIT_PAGE_HEADER,
    BUILD_HELP_TEXT,
    BUILD_INDEX_PAGE_HEADER,
)
from core.config import templates
from core.utils import create_base_admin_context, create_breadcrumbs
from dependencies.auth import get_current_admin
from forms.building import BuildingForm
from models.users import User
from services.building import BuildingServise


app_prefix = "/admin/staff/locations/buildings"
form_template = f"{app_prefix}/form.html"
list_template = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[BUILD_HELP_TEXT])


# ========= Buildings =========
@router.get("/")
async def get_buildings_admin(
    request: Request, msg: str = None, user: User = Depends(get_current_admin)
):
    records = await BuildingServise.all()

    # Создаем базовый контекст
    context = create_base_admin_context(
        request, BUILD_INDEX_PAGE_HEADER, BUILD_HELP_TEXT, user
    )
    context.update(
        {
            "buildings": records,
            "counter": len(records),
            "msg": msg,
            "breadcrumbs": create_breadcrumbs(
                router, [BUILD_INDEX_PAGE_HEADER], ["get_buildings_admin"]
            ),
        }
    )

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_building_admin(request: Request, user: User = Depends(get_current_admin)):
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, BUILD_ADD_PAGE_HEADER, BUILD_HELP_TEXT, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [BUILD_INDEX_PAGE_HEADER, BUILD_ADD_PAGE_HEADER],
                ["get_buildings_admin", "add_buildings_admin"],
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
            redirect_url = request.url_for("get_buildings_admin").include_query_params(
                msg=f"Филиал '{building.name}' добавлен!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, BUILD_ADD_PAGE_HEADER, BUILD_HELP_TEXT, user
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
        request, BUILD_EDIT_PAGE_HEADER, BUILD_HELP_TEXT, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [BUILD_INDEX_PAGE_HEADER, BUILD_EDIT_PAGE_HEADER],
                ["get_buildings_admin", "edit_buildings_admin"],
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
            return responses.RedirectResponse(
                request.url_for("get_buildings_admin").include_query_params(
                    msg=f"Данные '{building.name}' успешно обновлены!"
                ),
                status_code=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    # Создаем базовый контекст
    context = create_base_admin_context(
        request, BUILD_EDIT_PAGE_HEADER, BUILD_HELP_TEXT, user
    )
    context.update(
        {
            "breadcrumbs": create_breadcrumbs(
                router,
                [BUILD_INDEX_PAGE_HEADER, BUILD_EDIT_PAGE_HEADER],
                ["get_buildings_admin", "edit_buildings_admin"],
            ),
        }
    )
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{building_id}/delete")
async def delete_building_admin(
    building_id: int, request: Request, user: User = Depends(get_current_admin)
):
    redirect_url = request.url_for("get_buildings_admin")
    redirect_status = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await BuildingServise.delete(building_id)
        redirect = request.url_for("get_buildings_admin").include_query_params(
            msg="Филиал удален!"
        )
        return responses.RedirectResponse(redirect, status_code=redirect_status)
    except Exception as e:
        redirect_url.include_query_params(errors={"non_field_error": e})
        return responses.RedirectResponse(redirect_url, status_code=redirect_status)
