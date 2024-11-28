from typing import Optional
from fastapi import APIRouter, Request, responses, status

from admin.constants import (
    EMP_ADD_PAGE_HEADER as add_page_header,
    EMP_EDIT_PAGE_HEADER as edit_page_header,
    EMP_HELP_TEXT as hepl_text,
    EMP_INDEX_PAGE_HEADER as index_page_header,
    EMP_CUSERS_PAGE_HEADER as index_cusers_page_header,
)
from core.config import templates
from core.utils import create_breadcrumbs
from services.users import UsersDAO


app_prefix = "/admin/users"
form_teplate = f"{app_prefix}/form.html"
detail_teplate = f"{app_prefix}/detail.html"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Users =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_users_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
):
    records, counter, total_records, total_pages = (
        await UsersDAO.all_with_pagination(
            sort=sort, q=q, page=page, limit=limit
        )
    )

    return templates.TemplateResponse(
        list_teplate,
        {
            "request": request,
            "employees": records,
            "counter": counter,
            "page_header": index_page_header,
            "page_header_help": hepl_text,
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": total_pages,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_page_header], ["get_users_admin"]
            ),
        },
    )


@router.get("/cryptography")
async def get_cusers_admin(
    request: Request,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    filter_version: Optional[int] = None,
    filter_department: Optional[int] = None,
):
    filters = {}

    if filter_department and filter_department > 0:
        filters["department_id"] = filter_department

    if filter_version and filter_version > 0:
        filters["cryptography_version_id"] = filter_version

    cryptography_users, total_cryptography_users = (
        await EmployeeServise.cryptography_users(q=q, sort=sort, filters=filters)
    )

    departments, _ = await DepartmentServise.all()
    versions, _ = await CVersionServise.all()

    return templates.TemplateResponse(
        crypto_user_list_template,
        {
            "request": request,
            "users": cryptography_users,
            "total_users": total_cryptography_users,
            "page_header": index_cusers_page_header,
            "page_header_help": hepl_text,
            "departments": departments,
            "versions": versions,
            "filter_version": filter_version,
            "filter_department": filter_department,
            "q": q,
            "sort": sort,
            "breadcrumbs": create_breadcrumbs(
                router, [index_cusers_page_header], ["get_employees_admin"]
            ),
        },
    )


@router.get("/add")
async def add_employee_admin(request: Request):
    departments, _ = await DepartmentServise.all()
    positions, _ = await PositionServise.all()
    locations, _ = await LocationServise.all(sort="name")
    organisation = await OrganisationServise.all()
    return templates.TemplateResponse(
        form_teplate,
        context={
            "request": request,
            "page_header": add_page_header,
            "page_header_help": hepl_text,
            "departments": departments,
            "positions": positions,
            "locations": locations,
            "organisation": organisation,
            "is_created": True,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, add_page_header],
                ["get_employees_admin", "add_employee_admin"],
            ),
        },
    )


@router.post("/add")
async def create_employee_admin(request: Request):
    organisation = await OrganisationServise.all()
    form = EmployeeForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            emp = await EmployeeServise.add(
                name=form.name,
                surname=form.surname,
                middle_name=form.middle_name,
                position_id=int(form.position_id),
                department_id=int(form.department_id),
                location_id=int(form.location_id),
                organisation_id=organisation.id,
            )
            redirect_url = request.url_for("get_employees_admin").include_query_params(
                msg=f"Сотрудник '{emp.short_name}' добавлен!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    departments, _ = await DepartmentServise.all()
    positions, _ = await PositionServise.all()
    locations, _ = await LocationServise.all()
    context = {
        "page_header": add_employee_admin,
        "page_header_help": hepl_text,
        "departments": departments,
        "positions": positions,
        "locations": locations,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_employees_admin", "add_employee_admin"],
        ),
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{employee_id}")
async def detail_employee_admin(employee_id: int, request: Request):
    employee = await EmployeeServise.get_by_id(employee_id)
    return templates.TemplateResponse(
        detail_teplate,
        {
            "request": request,
            "employee": employee,
            "key_documents_total": 0,
            "page_header": employee.short_name,
            "page_header_help": hepl_text,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, employee.short_name],
                ["get_employees_admin", "detail_employee_admin"],
            ),
        },
    )


@router.get("/{employee_id}/edit")
async def edit_employee_admin(employee_id: int, request: Request):
    emp = await EmployeeServise.get_by_id(employee_id)
    departments, _ = await DepartmentServise.all()
    positions, _ = await PositionServise.all()
    locations, _ = await LocationServise.all()
    organisation = await OrganisationServise.all()
    key_documents, _ = await EmployeePersonalAccountService.all()
    return templates.TemplateResponse(
        form_teplate,
        {
            "request": request,
            "surname": emp.surname,
            "name": emp.name,
            "middle_name": emp.middle_name,
            "is_worked": emp.is_worked,
            "is_security_staff": emp.is_security_staff,
            "position_id": emp.position_id,
            "department_id": emp.department_id,
            "organisation_id": emp.organisation_id,
            "location_id": emp.location_id,
            "departments": departments,
            "positions": positions,
            "locations": locations,
            "organisation": organisation,
            "key_documents": key_documents,
            "page_header": edit_page_header,
            "page_header_help": hepl_text,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, edit_page_header],
                ["get_employees_admin", "edit_employee_admin"],
            ),
        },
    )


@router.post("/{employee_id}/edit")
async def update_employee_admin(employee_id: int, request: Request):
    form = EmployeeForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await EmployeeServise.update(
                employee_id,
                name=form.name,
                surname=form.surname,
                middle_name=form.middle_name,
                position_id=int(form.position_id),
                department_id=int(form.department_id),
                location_id=int(form.location_id),
                is_security_staff=True if form.is_security_staff == "on" else False,
            )
            redirect_url = request.url_for("get_employees_admin").include_query_params(
                msg=f"Данные сотрудника '{obj}' обновлены!"
            )
            return responses.RedirectResponse(
                redirect_url, status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            form.errors.setdefault("non_field_error", e)

    departments, _ = await DepartmentServise.all()
    positions, _ = await PositionServise.all()
    locations, _ = await LocationServise.all()
    organisation = await OrganisationServise.all()
    context = {
        "page_header_text": add_employee_admin,
        "page_header_help_text": hepl_text,
        "departments": departments,
        "positions": positions,
        "locations": locations,
        "organisation": organisation,
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{employee_id}/personal-account/doc")
async def download_personal_account_admin(employee_id: int, request: Request):
    employee = await EmployeeServise.get_by_id(employee_id)
    items, _ = await EmployeePersonalAccountService.get_by_user(employee_id)

    return create_file_response(
        LogbookTemplatesEnum.PERSONAL_LOGBOOK.value,
        {"employee": employee, "items": items},
        f"Лицевой счёт пользователя СКЗИ - {employee.short_name}",
    )


@router.get("/cryptography/doc")
async def download_cusers_admin(request: Request):
    items, _ = await EmployeeServise.cryptography_users()

    return create_file_response(
        LogbookTemplatesEnum.C_USERS_LOGBOOK.value,
        {"items": items},
        f"Список пользователей СКЗИ на дату - {get_str_now_date()}",
    )