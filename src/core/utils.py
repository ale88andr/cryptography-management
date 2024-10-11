import os
from fastapi import APIRouter, responses

from core.config import BASE_DIR
from core.templater import RenderTemplate


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
            bc.append({"title": titles[i], "url": router.url_path_for(urls[i]) if i < t_len-1 else None})

    return bc


def create_file_response(template, context, name):
    from io import BytesIO

    docx_in_memory = BytesIO()
    template = os.path.join(BASE_DIR, "media/doc", template)
    content_disposition = f"attachment; filename={name.encode('utf-8').decode('unicode-escape')}.docx"

    RenderTemplate(template, context, docx_in_memory)

    docx_in_memory.seek(0)

    return responses.StreamingResponse(
        content=docx_in_memory,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": content_disposition}
    )
