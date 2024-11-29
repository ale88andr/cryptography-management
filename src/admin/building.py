from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    BUILD_ADD_PAGE_HEADER,
    BUILD_EDIT_PAGE_HEADER,
    BUILD_HELP_TEXT,
    BUILD_INDEX_PAGE_HEADER,
)
from core.config import templates
from core.utils import add_breadcrumb
from dependencies.auth import get_current_admin
from models.users import User
from services.building import BuildingServise


app_prefix = "/admin/staff/locations/buildings"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[BUILD_HELP_TEXT])


# ========= Buildings =========
@router.get("/")
async def get_buildings_admin(request: Request, msg: str = None, user: User = Depends(get_current_admin)):
    records = await BuildingServise.all()
    return templates.TemplateResponse(
        list_teplate,
        context={
            "request": request,
            "buildings": records,
            "counter": len(records),
            "msg": msg,
            "page_header": BUILD_INDEX_PAGE_HEADER,
            "page_header_help": BUILD_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(
                    router, BUILD_INDEX_PAGE_HEADER, "get_buildings_admin", True
                ),
            ],
            "user": user
        },
    )


@router.get("/add")
async def add_building_admin(request: Request, user: User = Depends(get_current_admin)):
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header": BUILD_ADD_PAGE_HEADER,
            "page_header_help": BUILD_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, BUILD_INDEX_PAGE_HEADER, "get_buildings_admin"),
                add_breadcrumb(
                    router, BUILD_ADD_PAGE_HEADER, "add_buildings_admin", True
                ),
            ],
            "user": user
        },
    )


@router.post("/add")
async def create_building_admin(request: Request, user: User = Depends(get_current_admin)):
    context = {
        "page_header": BUILD_ADD_PAGE_HEADER,
        "page_header_help": BUILD_HELP_TEXT,
        "user": user
    }
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
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{building_id}/edit")
async def edit_building_admin(building_id: int, request: Request, user: User = Depends(get_current_admin)):
    organisation = await BuildingServise.get_one_or_none(id=building_id)
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "name": organisation.name,
            "city": organisation.city,
            "street": organisation.street,
            "building": organisation.building,
            "index": organisation.index,
            "page_header": BUILD_EDIT_PAGE_HEADER,
            "page_header_help": BUILD_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, BUILD_INDEX_PAGE_HEADER, "get_buildings_admin"),
                add_breadcrumb(
                    router, BUILD_EDIT_PAGE_HEADER, "edit_building_admin", True
                ),
            ],
            "user": user
        },
    )


@router.post("/{building_id}/edit")
async def update_building_admin(building_id: int, request: Request, user: User = Depends(get_current_admin)):
    context = {
        "page_header": BUILD_EDIT_PAGE_HEADER,
        "page_header_help": BUILD_HELP_TEXT,
        "user": user
    }
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
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{building_id}/delete")
async def delete_building_admin(building_id: int, request: Request, user: User = Depends(get_current_admin)):
    redirect_url = request.url_for("get_buildings_admin")
    try:
        await BuildingServise.delete(building_id)
        redirect = request.url_for("get_buildings_admin").include_query_params(
            msg="Филиал удален!"
        )
        return responses.RedirectResponse(
            redirect, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    except Exception as e:
        redirect_url.include_query_params(errors={"non_field_error": e})
        return responses.RedirectResponse(
            redirect_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )


class BuildingForm:
    REQUIRED_ERROR = "Поле должно быть заполнено!"

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict = {}
        self.name: str
        self.city: str
        self.street: str
        self.building: str
        self.index: int

    async def load_data(self):
        form = await self.request.form()
        self.name: str = form.get("name")
        self.city: str = form.get("city")
        self.street: str = form.get("street")
        self.building: str = form.get("building")
        self.index: int = form.get("index")

    async def is_valid(self):
        name_min_length = 3
        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if not self.city:
            self.errors.setdefault("city", self.REQUIRED_ERROR)
        if not self.street:
            self.errors.setdefault("street", self.REQUIRED_ERROR)
        if not self.building:
            self.errors.setdefault("building", self.REQUIRED_ERROR)
        if self.index and not self.index.isnumeric():
            self.errors.setdefault("index", self.REQUIRED_ERROR)

        if not self.errors:
            return True
        return False
