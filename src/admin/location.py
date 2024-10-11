from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    LOC_ADD_PAGE_HEADER,
    LOC_EDIT_PAGE_HEADER,
    LOC_INDEX_PAGE_HEADER,
    LOC_HELP_TEXT,
)
from core.config import templates
from core.utils import add_breadcrumb
from services.building import BuildingServise
from services.location import LocationServise


app_prefix = "/admin/staff/locations"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[LOC_HELP_TEXT])


# ========= Locations =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_locations_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_building_id: Optional[int] = None,
):
    filters = {}
    if filter_building_id and filter_building_id > 0:
        filters["building_id"] = filter_building_id

    records, counter = await LocationServise.all(sort=sort, q=q, filters=filters)
    buildings = await BuildingServise.all()

    return templates.TemplateResponse(
        list_teplate,
        context={
            "request": request,
            "locations": records,
            "buildings": buildings,
            "counter": counter,
            "filter_building_id": filter_building_id,
            "page_header": LOC_INDEX_PAGE_HEADER,
            "page_header_help": LOC_HELP_TEXT,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": [
                add_breadcrumb(
                    router, LOC_INDEX_PAGE_HEADER, "get_locations_admin", True
                )
            ],
        },
    )


@router.get("/add")
async def add_location_admin(request: Request):
    buildings = await BuildingServise.all()
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header": LOC_ADD_PAGE_HEADER,
            "page_header_help": LOC_HELP_TEXT,
            "buildings": buildings,
            "breadcrumbs": [
                add_breadcrumb(router, LOC_INDEX_PAGE_HEADER, "get_locations_admin"),
                add_breadcrumb(router, LOC_ADD_PAGE_HEADER, "add_location_admin", True),
            ],
        },
    )


@router.post("/add")
async def create_loc_admin(request: Request):
    form = LocationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            loc = await LocationServise.add(
                name=form.name, building_id=int(form.building_id)
            )
            redirect_url = request.url_for("get_locations_admin").include_query_params(
                msg=f"Рабочее место '{loc.name}' создано!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    context = {
        "page_header_text": LOC_ADD_PAGE_HEADER,
        "page_header_help_text": LOC_HELP_TEXT,
        "buildings": await BuildingServise.all(),
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{location_id}/edit")
async def edit_location_admin(location_id: int, request: Request):
    loc = await LocationServise.get_by_id(location_id)
    buildings = await BuildingServise.all()
    return templates.TemplateResponse(
        form_teplate,
        {
            "request": request,
            "name": loc.name,
            "building_id": loc.building_id,
            "buildings": buildings,
            "page_header": LOC_EDIT_PAGE_HEADER,
            "page_header_help": LOC_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, LOC_INDEX_PAGE_HEADER, "get_locations_admin"),
                add_breadcrumb(
                    router, LOC_EDIT_PAGE_HEADER, "edit_locations_admin", True
                ),
            ],
        },
    )


@router.post("/{location_id}/edit")
async def update_location_admin(location_id: int, request: Request):
    form = LocationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            loc = await LocationServise.update(
                location_id, name=form.name, building_id=int(form.building_id)
            )
            redirect_url = request.url_for("get_locations_admin").include_query_params(
                msg=f"Рабочее место '{loc.name}' обновлено!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    context = {
        "page_header_text": LOC_EDIT_PAGE_HEADER,
        "page_header_help_text": LOC_HELP_TEXT,
        "buildings": await BuildingServise.all(),
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{location_id}/delete")
async def delete_location_admin(location_id: int, request: Request):
    redirect_url = request.url_for("get_locations_admin")
    redirect_code = status.HTTP_307_TEMPORARY_REDIRECT
    try:
        await LocationServise.delete(location_id)
        redirect_url = redirect_url.include_query_params(msg="Рабочее место удалено!")
    except Exception as e:
        redirect_url = redirect_url.include_query_params(errors={"non_field_error": e})

    return responses.RedirectResponse(redirect_url, status_code=redirect_code)


class LocationForm:
    REQUIRED_ERROR = "Поле должно быть заполнено!"

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict = {}
        self.name: str
        self.building_id: int

    async def load_data(self):
        form = await self.request.form()
        self.name: str = form.get("name")
        self.building_id: int = form.get("building_id")

    async def is_valid(self):
        name_min_length = 3
        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if self.name:
            db_loc = await LocationServise.get_one_or_none(name=self.name)
            if db_loc and db_loc.building_id == int(self.building_id):
                self.errors.setdefault(
                    "name", f"'{self.name}' - Такое рабочее место уже существует!"
                )
        if not self.building_id or not self.building_id.isnumeric():
            self.errors.setdefault("building_id", self.REQUIRED_ERROR)

        if not self.errors:
            return True
        return False
