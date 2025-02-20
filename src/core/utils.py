from ast import Dict
import os
from typing import Optional
from fastapi import APIRouter, responses, Request, status

from core.config import BASE_DIR
from core.templater import RenderTemplate
from models.users import User


def add_breadcrumb(
    router: APIRouter, title: str, route: str, is_active: bool = False
) -> dict[str, str]:
    bc_dict = {"title": title}
    if not is_active:
        bc_dict["url"] = router.url_path_for(route)
    return bc_dict


def create_breadcrumbs(router: APIRouter, titles: list, urls: list) -> list:
    bc, t_len = [], len(titles)
    if t_len == len(urls):
        for i in range(t_len):
            bc.append(
                {
                    "title": titles[i],
                    "url": router.url_path_for(urls[i]) if i < t_len - 1 else None,
                }
            )

    return bc


def create_file_response(template, context, name):
    from io import BytesIO

    docx_in_memory = BytesIO()
    template = os.path.join(BASE_DIR, "media/doc", template)
    content_disposition = (
        f"attachment; filename={name.encode('utf-8').decode('unicode-escape')}.docx"
    )

    RenderTemplate(template, context, docx_in_memory)

    docx_in_memory.seek(0)

    return responses.StreamingResponse(
        content=docx_in_memory,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": content_disposition},
    )


def get_bool_from_checkbox(param: str) -> bool:
    return True if param == "on" else False


def create_base_admin_context(
    request: Request,
    page_header: str,
    page_header_help: str,
    user: User) -> dict:
    """Создает базовый контекст для HTML страниц админ панели"""
    return {
        "request": request,
        "page_header": page_header,
        "page_header_help": page_header_help,
        "user": user,
    }


def redirect_with_message(
    request: Request,
    endpoint: str,
    msg: str,
    status: status=status.HTTP_303_SEE_OTHER
) -> responses.RedirectResponse:
    """Редирект с сообщением"""
    redirect_url = request.url_for(endpoint).include_query_params(msg=msg)
    return responses.RedirectResponse(redirect_url, status_code=status)


def redirect_with_error(
    request: Request,
    endpoint: str,
    errors: dict,
    status: status=status.HTTP_307_TEMPORARY_REDIRECT
) -> responses.RedirectResponse:
    """Редирект с ошибкой"""
    redirect_url = request.url_for(endpoint).include_query_params(errors=errors)
    return responses.RedirectResponse(redirect_url, status_code=status)

def redirect(
    request: Request,
    endpoint: str,
    msg: Optional[str]=None,
    errors: Optional[Dict]=None
) -> responses.RedirectResponse:
    """Редирект с возможностью добавления сообщения или ошибок"""
    redirect_url = request.url_for(endpoint)
    status_code = status.HTTP_303_SEE_OTHER

    if msg:
        redirect_url = redirect_url.include_query_params(msg=msg)
    elif errors:
        redirect_url = redirect_url.include_query_params(errors=errors)
        status_code = status.HTTP_307_TEMPORARY_REDIRECT

    return responses.RedirectResponse(url=redirect_url, status_code=status_code)
