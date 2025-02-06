from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    EMP_ADD_PAGE_HEADER as add_page_header,
    EMP_EDIT_PAGE_HEADER as edit_page_header,
    EMP_HELP_TEXT as hepl_text,
    EMP_INDEX_PAGE_HEADER as index_page_header,
    EMP_CUSERS_PAGE_HEADER as index_cusers_page_header,
    EMP_DISMISS_PAGE_HEADER as termination_page_header
)
from core.config import templates
from core.utils import create_breadcrumbs, create_file_response, redirect_with_message
from core.templater import LogbookTemplatesEnum
from dependencies.auth import get_current_admin
from models.logbook import ActRecordTypes
from models.users import User
from services.c_version import CVersionServise
from services.c_action import CActionServise
from services.department import DepartmentServise
from services.employee import EmployeeServise
from services.key_document import KeyDocumentServise
from services.location import LocationServise
from services.organisation import OrganisationServise
from services.position import PositionServise
from services.employee_personal_account import EmployeePersonalAccountService
from forms.employee import EmployeeForm
from forms.destruction import DestructionForm
from utils.formatting import get_str_now_date, format_date


app_prefix = "/admin/staff/employees"
form_teplate = f"{app_prefix}/form.html"
form_termination_template = f"{app_prefix}/termination_form.html"
detail_teplate = f"{app_prefix}/detail.html"
list_teplate = f"{app_prefix}/index.html"
crypto_user_list_template = f"{app_prefix}/users.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Employees =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_employees_admin(
    request: Request,
    msg: str = None,
    page: int = 0,
    limit: int = 20,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    filter_position: Optional[int] = None,
    filter_department: Optional[int] = None,
    filter_location: Optional[int] = None,
    user: User = Depends(get_current_admin)
):
    filters = {}

    if filter_position and filter_position > 0:
        filters["position_id"] = filter_position

    if filter_department and filter_department > 0:
        filters["department_id"] = filter_department

    if filter_location and filter_location > 0:
        filters["location_id"] = filter_location

    records, counter, total_records, total_pages = (
        await EmployeeServise.all_with_pagination(
            sort=sort, q=q, page=page, limit=limit, filters=filters
        )
    )
    departments, _ = await DepartmentServise.all()
    positions, _ = await PositionServise.all()
    locations, _ = await LocationServise.all()

    return templates.TemplateResponse(
        list_teplate,
        {
            "request": request,
            "employees": records,
            "counter": counter,
            "departments": departments,
            "positions": positions,
            "locations": locations,
            "page_header": index_page_header,
            "page_header_help": hepl_text,
            "filter_position": filter_position,
            "filter_department": filter_department,
            "filter_location": filter_location,
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": total_pages,
            "msg": msg,
            "sort": sort,
            "q": q,
            "breadcrumbs": create_breadcrumbs(
                router, [index_page_header], ["get_employees_admin"]
            ),
            "user": user
        },
    )


@router.get("/cryptography")
async def get_cusers_admin(
    request: Request,
    q: Optional[str] = None,
    sort: Optional[str] = None,
    filter_version: Optional[int] = None,
    filter_department: Optional[int] = None,
    user: User = Depends(get_current_admin)
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
            "user": user
        },
    )


@router.get("/add")
async def add_employee_admin(request: Request, user: User = Depends(get_current_admin)):
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
            "is_create": True,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, add_page_header],
                ["get_employees_admin", "add_employee_admin"],
            ),
            "user": user
        },
    )


@router.post("/add")
async def create_employee_admin(request: Request, user: User = Depends(get_current_admin)):
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
            return redirect_with_message(
                request=request,
                endpoint="get_employees_admin",
                msg=f"Сотрудник '{emp.short_name}' добавлен!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)

    departments, _ = await DepartmentServise.all()
    positions, _ = await PositionServise.all()
    locations, _ = await LocationServise.all()
    context = {
        "page_header": add_page_header,
        "page_header_help": hepl_text,
        "departments": departments,
        "positions": positions,
        "locations": locations,
        "breadcrumbs": create_breadcrumbs(
            router,
            [index_page_header, add_page_header],
            ["get_employees_admin", "add_employee_admin"],
        ),
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{employee_id}")
async def detail_employee_admin(employee_id: int, request: Request, user: User = Depends(get_current_admin)):
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
            "user": user
        },
    )


@router.get("/{employee_id}/edit")
async def edit_employee_admin(employee_id: int, request: Request, user: User = Depends(get_current_admin)):
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
            "user": user
        },
    )


@router.post("/{employee_id}/edit")
async def update_employee_admin(employee_id: int, request: Request, user: User = Depends(get_current_admin)):
    form = EmployeeForm(request, is_create=False)
    await form.load_data()
    if await form.is_valid():
        try:
            if form.is_worked:
                obj = await EmployeeServise.update(
                    employee_id, is_worked=bool(form.is_worked == "on")
                )
            else:
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
            return redirect_with_message(
                request=request,
                endpoint="get_employees_admin",
                msg=f"Данные сотрудника '{obj}' обновлены!"
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
        "user": user
    }
    context.update(form.__dict__)
    context.update(form.fields)
    return templates.TemplateResponse(form_teplate, context)


@router.get("/{pk}/termination")
async def termination_employee_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
    employee = await EmployeeServise.get_by_id(pk)
    key_documents, key_documents_counter = await EmployeePersonalAccountService.get_by_user(employee.id, only_active=True)
    staff_members = await EmployeeServise.get_short_list(is_staff=True)

    return templates.TemplateResponse(
        form_termination_template,
        {
            "request": request,
            "employee": employee,
            "key_documents": key_documents,
            "key_documents_counter": key_documents_counter,
            "staff_members": staff_members,
            "page_header": termination_page_header,
            "page_header_help": hepl_text,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, termination_page_header],
                ["get_employees_admin", "termination_employee_admin"],
            ),
            "user": user
        },
    )


@router.post("/{pk}/termination")
async def terminate_employee_admin(pk: int, request: Request, user: User = Depends(get_current_admin)):
    employee = await EmployeeServise.get_by_id(pk)
    user_cryptography_keys, key_count = await KeyDocumentServise.all(
        filters={"owner_id": employee.id, "remove_act_record_id": None}
    )

    if key_count == 0:
        await EmployeeServise.update(employee.id, is_worked=False)
        return redirect_with_message(
            request, "get_employees_admin", "Сотрудник уволен!"
        )
    else:
        form = DestructionForm(request, is_create=False)
        await form.load_data()
        if await form.is_valid():
            try:
                action_date = format_date(form.action_date)

                # Запись данных акта об изъятии
                log_action = await CActionServise.add_record(
                    ActRecordTypes.I_REMOVE,
                    action_date,
                    form.head_commision_member_id,
                    form.commision_member_id,
                    form.performer_id,
                    form.reason,
                    format_date(form.reason_date),
                )

                await EmployeeServise.terminate_employee(
                    employee=employee,
                    keys=user_cryptography_keys,
                    act_record=log_action,
                    action_date=action_date,
                )
                return redirect_with_message(
                    request=request,
                    endpoint="get_employees_admin",
                    msg="Сотрудник уволен, ключевая информация изъята(уничтожена)!"
                )
            except Exception as e:
                print("-------------------------------")
                print(e)
                print("-------------------------------")
                form.errors.setdefault("non_field_error", e)

        staff_members = await EmployeeServise.get_short_list(is_staff=True)
        key_documents, key_documents_counter = await EmployeePersonalAccountService.get_by_user(employee.id, only_active=True)
        context = {
            "request": request,
            "employee": employee,
            "page_header": termination_page_header,
            "page_header_help": hepl_text,
            "staff_members": staff_members,
            "responsible_user_cryptography_keys": user_cryptography_keys,
            "head_commision_member_id": None,
            "commision_member_id": None,
            "performer_id": None,
            "key_documents": key_documents,
            "key_documents_counter": key_documents_counter,
            "breadcrumbs": create_breadcrumbs(
                router,
                [index_page_header, termination_page_header],
                ["get_employees_admin", "termination_employee_admin"],
            ),
            "user": user
        }
        context.update(form.__dict__)
        context.update(form.fields)
        return templates.TemplateResponse(form_termination_template, context)


@router.get("/{employee_id}/personal-account/doc")
async def download_personal_account_admin(employee_id: int, request: Request, user: User = Depends(get_current_admin)):
    employee = await EmployeeServise.get_by_id(employee_id)
    items, _ = await EmployeePersonalAccountService.get_by_user(employee_id)

    return create_file_response(
        LogbookTemplatesEnum.PERSONAL_LOGBOOK.value,
        {"employee": employee, "items": items},
        f"Лицевой счёт пользователя СКЗИ - {employee.short_name}",
    )


@router.get("/cryptography/doc")
async def download_cusers_admin(request: Request, user: User = Depends(get_current_admin)):
    items, _ = await EmployeeServise.cryptography_users()

    return create_file_response(
        LogbookTemplatesEnum.C_USERS_LOGBOOK.value,
        {"items": items},
        f"Список пользователей СКЗИ на дату - {get_str_now_date()}",
    )
