import calendar
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, responses

from admin.constants import (
    CILOG_HELP_TEXT as hepl_text,
    CILOG_INDEX_PAGE_HEADER as index_page_header,
    CILOG_ADD_PAGE_HEADER as add_page_header,
)
from core.config import templates
from services.c_action import CActionServise
from services.carrier_types import CarrierTypesServise
from services.key_carrier import KeyCarrierServise
from services.key_document import KeyDocumentServise
from services.employee import EmployeeServise
from services.c_version import CVersionServise
from services.organisation import OrganisationServise


app_prefix = "/admin"
list_teplate = f"{app_prefix}/index.html"

router = APIRouter(prefix=app_prefix, tags=[hepl_text])


# ========= Cryptography Models Versions =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_dashboard_admin(
    request: Request,
    msg: str = None,
    q: Optional[str] = None,
    filter_model_id: Optional[int] = None,
    filter_grade: Optional[int] = None,
):
    latest_users, total_users = await EmployeeServise.latest_cryptography_users(limit=5)
    latest_logbook = await KeyDocumentServise.latest(limit=10)

    today_users = await EmployeeServise.today_cryptography_users()
    month_users = await EmployeeServise.month_cryptography_users()

    total_keys = await KeyDocumentServise.count_keys()
    today_keys = await KeyDocumentServise.count_today_keys()
    month_keys = await KeyDocumentServise.count_month_keys()

    total_versions = await CVersionServise.count()
    total_unused_versions = await CVersionServise.count_unused()

    now = datetime.utcnow()
    total_year_action = await CActionServise.count()
    total_year_install = await CActionServise.count_install()
    total_year_remove = await CActionServise.count_remove()

    key_versions = await CVersionServise.count_by_versions()
    installs_by_month = await CActionServise.count_by_month()
    count_key_carriers = await KeyCarrierServise.count_key_carriers()

    organisation = await OrganisationServise.all()

    context = {
        "request": request,
        "latest_users": latest_users,
        "total_users": total_users,
        "today_users": today_users,
        "month_users": month_users,
        "today_keys": today_keys,
        "month_keys": month_keys,
        "total_keys": total_keys,
        "total_versions": total_versions,
        "total_unused_versions": total_unused_versions,
        "now": now,
        "organisation": organisation,
        "version_chart_labels": [item[0].title for item in key_versions],
        "version_chart_data": [item[1] for item in key_versions],
        "act_chart_labels": [
            calendar.month_abbr[int(item[0])] for item in installs_by_month
        ],
        "act_chart_data": [str(item[1]) for item in installs_by_month],
        "carrier_chart_labels": [str(item[0]) for item in count_key_carriers],
        "carrier_chart_data": [str(item[1]) for item in count_key_carriers],
        "total_year_action": total_year_action,
        "total_year_install": total_year_install,
        "total_year_remove": total_year_remove,
        "latest_logbook": latest_logbook,
        "page_header": index_page_header,
        "add_page_header": add_page_header,
        "page_header_help": hepl_text,
        "filter_model_id": filter_model_id,
        "filter_grade": filter_grade,
        "msg": msg,
        "q": q,
    }
    return templates.TemplateResponse(list_teplate, context)
