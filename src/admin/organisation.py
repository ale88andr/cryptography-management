from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ORG_ADD_HEADER as add_header,
    ORG_EDIT_HEADER as edit_header,
    ORG_INDEX_PAGE_HEADER as index_header,
    OGR_HELP_TEXT as help_text,
)
from core.config import templates
from core.templater import DocumentTemplatesEnum
from core.utils import (
    create_base_admin_context,
    create_breadcrumbs,
    create_file_response,
    redirect_with_message,
)
from dependencies.auth import get_current_admin
from forms.organisation import OrganisationForm
from models.users import User
from services.organisation import OrganisationServise
from services.employee import EmployeeServise


app_prefix = "/admin/staff/organisations"
form_template = f"{app_prefix}/form.html"
list_template = f"{app_prefix}/organisation.html"

router = APIRouter(prefix=app_prefix, tags=[help_text])


# ========= Organisations =========
@router.get("/")
async def get_organisation_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    organisation = await OrganisationServise.all()
    if not organisation:
        return responses.RedirectResponse(
            request.url_for("add_organisation_admin"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update({
        "organisation": organisation,
        "breadcrumbs": create_breadcrumbs(
            router, [index_header], ["get_organisation_admin"]
        ),
    })

    return templates.TemplateResponse(list_template, context)


@router.get("/add")
async def add_organisation_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    # Создаем базовый контекст
    context = create_base_admin_context(request, index_header, help_text, user)
    context.update({
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, add_header],
            ["get_organisation_admin", "add_organisation_admin"],
        ),
    })

    return templates.TemplateResponse(form_template, context)


@router.post("/add")
async def create_organisation_admin(
    request: Request, user: User = Depends(get_current_admin)
):
    form = OrganisationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            organisation = await OrganisationServise.add(
                name=form.name,
                short_name=form.short_name,
                chief=form.chief,
                city=form.city,
                street=form.street,
                building=form.building,
                index=int(form.index),
            )
            return redirect_with_message(
                request,
                "get_organisations_admin",
                msg=f"Организация '{organisation.name}' успешно создана!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    # Создаем базовый контекст
    context = create_base_admin_context(request, add_header, help_text, user)
    context.update({
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, add_header],
            ["get_organisation_admin", "add_organisation_admin"],
        ),
    })
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/{organisation_id}/edit")
async def edit_organisation_admin(
    organisation_id: int, request: Request, user: User = Depends(get_current_admin)
):
    organisation = await OrganisationServise.get_one_or_none(id=organisation_id)
    employees = await EmployeeServise.get_short_list(is_staff=True)
    employees_chief = await EmployeeServise.get_short_list(is_leadership=True)

    # Создаем базовый контекст
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update({
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, edit_header],
            ["get_organisation_admin", "edit_organisation_admin"],
        ),
        "employees": employees,
        "employees_chief": employees_chief,
        **vars(organisation),
    })

    return templates.TemplateResponse(form_template, context)


@router.post("/{organisation_id}/edit")
async def update_organisation_admin(
    organisation_id: int, request: Request, user: User = Depends(get_current_admin)
):
    form = OrganisationForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            organisation = await OrganisationServise.update(
                organisation_id,
                name=form.name,
                short_name=form.short_name,
                chief=form.chief,
                chief_id=form.chief_id,
                city=form.city,
                street=form.street,
                building=form.building,
                index=int(form.index),
                responsible_employee_id=form.responsible_employee_id,
                spare_responsible_employee_id=form.spare_responsible_employee_id,
            )
            return redirect_with_message(
                request,
                "get_organisation_admin",
                msg=f"Данные '{organisation.name}' обновлены!",
                status=status.HTTP_303_SEE_OTHER,
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)

    # Создаем базовый контекст
    employees = await EmployeeServise.get_short_list(is_staff=True)
    employees_chief = await EmployeeServise.get_short_list(is_leadership=True)
    context = create_base_admin_context(request, edit_header, help_text, user)
    context.update({
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_header, edit_header],
            ["get_organisation_admin", "edit_organisation_admin"],
        ),
        "employees": employees,
        "employees_chief": employees_chief,
    })
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_template, context)


@router.get("/order")
async def download_appointment_order_admin(request: Request, user: User = Depends(get_current_admin)):
    organisation = await OrganisationServise.all()

    return create_file_response(
        DocumentTemplatesEnum.APPOINTMENT_ORDER.value,
        {"org": organisation},
        f"Приказ о назначении ответственного за эксплуатацию",
    )
