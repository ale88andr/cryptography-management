from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    ORG_ADD_HEADER,
    ORG_EDIT_HEADER,
    ORG_INDEX_PAGE_HEADER,
    OGR_HELP_TEXT,
)
from core.config import templates
from core.utils import add_breadcrumb
from services.organisation import OrganisationServise


app_prefix = "/admin/staff/organisations"
form_teplate = f"{app_prefix}/form.html"
list_teplate = f"{app_prefix}/organisation.html"

router = APIRouter(prefix=app_prefix, tags=[OGR_HELP_TEXT])


# ========= Organisations =========
@router.get("/")
async def get_organisation_admin(request: Request):
    organisation = await OrganisationServise.all()
    if not organisation:
        return responses.RedirectResponse(
            request.url_for("add_organisation_admin"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return templates.TemplateResponse(
        list_teplate,
        context={
            "request": request,
            "organisation": organisation,
            "page_header": ORG_INDEX_PAGE_HEADER,
            "page_header_help": OGR_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(
                    router,
                    ORG_INDEX_PAGE_HEADER,
                    "get_organisation_admin",
                    is_active=True,
                ),
            ],
        },
    )


@router.get("/add")
async def add_organisation_admin(request: Request):
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header": ORG_ADD_HEADER,
            "page_header_help": OGR_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, ORG_INDEX_PAGE_HEADER, "get_organisation_admin"),
                add_breadcrumb(router, ORG_ADD_HEADER, "add_organisation_admin", True),
            ],
        },
    )


@router.post("/add")
async def create_organisation_admin(request: Request):
    context = {
        "page_header": "Добавление должности",
        "page_header_help": "Администрирование должностей сотрудников",
    }
    form = OrganisationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            organisation = await OrganisationServise.create(
                name=form.name,
                short_name=form.short_name,
                chief=form.chief,
                city=form.city,
                street=form.street,
                building=form.building,
                index=int(form.index),
            )
            redirect_url = request.url_for(
                "get_organisations_admin"
            ).include_query_params(
                msg=f"Организация '{organisation.name}' успешно создана!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    print(context)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{organisation_id}/edit")
async def edit_organisation_admin(organisation_id: int, request: Request):
    organisation = await OrganisationServise.get_one_or_none(id=organisation_id)
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "name": organisation.name,
            "short_name": organisation.short_name,
            "city": organisation.city,
            "street": organisation.street,
            "building": organisation.building,
            "index": organisation.index,
            "chief": organisation.chief,
            "page_header": ORG_EDIT_HEADER,
            "page_header_help": OGR_HELP_TEXT,
            "breadcrumbs": [
                add_breadcrumb(router, ORG_INDEX_PAGE_HEADER, "get_organisation_admin"),
                add_breadcrumb(
                    router, ORG_EDIT_HEADER, "edit_organisation_admin", True
                ),
            ],
        },
    )


@router.post("/{organisation_id}/edit")
async def update_organisation_admin(organisation_id: int, request: Request):
    context = {
        "page_header": ORG_EDIT_HEADER,
        "page_header_help": OGR_HELP_TEXT,
    }
    form = OrganisationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            organisation = await OrganisationServise.update(
                organisation_id,
                name=form.name,
                short_name=form.short_name,
                chief=form.chief,
                city=form.city,
                street=form.street,
                building=form.building,
                index=int(form.index),
            )
            redirect_url = request.url_for(
                "get_organisation_admin"
            ).include_query_params(msg=f"Данные '{organisation.name}' обновлены!")
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_teplate, form.__dict__)
    context.update(form.__dict__)
    return templates.TemplateResponse(form_teplate, context)


class OrganisationForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict = {}
        self.name: str
        self.short_name: str
        self.city: str
        self.street: str
        self.building: str
        self.index: int
        self.chief: str

    async def load_data(self):
        form = await self.request.form()
        self.name: str = form.get("name")
        self.short_name: str = form.get("short_name")
        self.city: str = form.get("city")
        self.street: str = form.get("street")
        self.building: str = form.get("building")
        self.index: int = form.get("index")
        self.chief: str = form.get("chief")

    async def is_valid(self):
        name_min_length = 3
        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if not self.short_name or not len(self.short_name) >= name_min_length:
            self.errors.setdefault(
                "short_name",
                f"Поле должно содержать как минимум {name_min_length} символа!",
            )
        if not self.city:
            self.errors.setdefault("city", "Поле должно быть заполнено!")
        if not self.building:
            self.errors.setdefault("building", "Поле должно быть заполнено!")
        if not self.chief:
            self.errors.setdefault("chief", "Поле должно быть заполнено!")
        if self.index and not self.index.isnumeric():
            self.errors.setdefault("index", "Поле должно состоять из цифр!")

        if not self.errors:
            return True
        return False
