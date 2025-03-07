from typing import Optional
from fastapi import APIRouter, Request, Depends, responses, status

from admin.constants import (
    ADMIN_CTYPE_ADD_HEADER,
    ADMIN_CTYPE_EDIT_HEADER,
    ADMIN_CTYPE_DESCRIPTION,
    ADMIN_CTYPE_INDEX_HEADER,
    ADMIN_CTYPE as app_prefix,
    ADMIN_CTYPE_FORM_TPL as form_template,
    ADMIN_CTYPE_LIST_TPL as list_template
)
from core.config import templates
from core.utils import add_breadcrumb, redirect, redirect_with_error, redirect_with_message
from dependencies.auth import get_current_admin
from models.users import User
from services.carrier_types import CarrierTypesServise
from services.key_carrier import KeyCarrierServise


router = APIRouter(prefix=app_prefix, tags=[ADMIN_CTYPE_DESCRIPTION])
index_url = "get_ctypes_admin"


# ========= Carrier types =========
@router.get("/", response_class=responses.HTMLResponse)
async def get_ctypes_admin(
    request: Request,
    msg: str = None,
    sort: Optional[str] = None,
    q: Optional[str] = None,
    error: Optional[str] = None,
    user: User = Depends(get_current_admin),
):
    records, counter = await CarrierTypesServise.all(sort=sort, q=q)
    return templates.TemplateResponse(
        list_template,
        context={
            "request": request,
            "objects": records,
            "counter": counter,
            "page_header": ADMIN_CTYPE_INDEX_HEADER,
            "page_header_help": ADMIN_CTYPE_DESCRIPTION,
            "msg": msg,
            "error": error,
            "sort": sort,
            "q": q,
            "breadcrumbs": [
                add_breadcrumb(
                    router,
                    ADMIN_CTYPE_INDEX_HEADER,
                    index_url,
                    is_active=True,
                )
            ],
            "user": user,
        },
    )


@router.get("/add")
async def add_ctype_admin(request: Request, user: User = Depends(get_current_admin)):
    return templates.TemplateResponse(
        form_template,
        context={
            "request": request,
            "page_header": ADMIN_CTYPE_ADD_HEADER,
            "page_header_help": ADMIN_CTYPE_DESCRIPTION,
            "breadcrumbs": [
                add_breadcrumb(router, ADMIN_CTYPE_INDEX_HEADER, index_url),
                add_breadcrumb(
                    router, ADMIN_CTYPE_ADD_HEADER, "add_ctype_admin", is_active=True
                ),
            ],
            "user": user,
        },
    )


@router.post("/add")
async def create_ctype_admin(request: Request, user: User = Depends(get_current_admin)):
    form = CtypeForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CarrierTypesServise.add(name=form.name)

            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Тип ключевого носителя '{obj.name}' создан!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    context = {
        "page_header_text": ADMIN_CTYPE_ADD_HEADER,
        "page_header_help_text": ADMIN_CTYPE_DESCRIPTION,
        "user": user,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.get("/{ctype_id}/edit")
async def edit_ctype_admin(
    ctype_id: int, request: Request, user: User = Depends(get_current_admin)
):
    obj = await CarrierTypesServise.get_by_id(ctype_id)
    return templates.TemplateResponse(
        form_template,
        context={
            "request": request,
            "name": obj.name,
            "page_header": ADMIN_CTYPE_EDIT_HEADER,
            "page_header_help": ADMIN_CTYPE_DESCRIPTION,
            "breadcrumbs": [
                add_breadcrumb(router, ADMIN_CTYPE_INDEX_HEADER, index_url),
                add_breadcrumb(
                    router, ADMIN_CTYPE_EDIT_HEADER, "edit_ctype_admin", is_active=True
                ),
            ],
            "user": user,
        },
    )


@router.post("/{ctype_id}/edit")
async def update_ctype_admin(
    ctype_id: int, request: Request, user: User = Depends(get_current_admin)
):
    form = CtypeForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            obj = await CarrierTypesServise.update(ctype_id, name=form.name)

            return redirect(
                request=request,
                endpoint=index_url,
                msg=f"Тип ключевого носителя '{obj.name}' обновлен!"
            )
        except Exception as e:
            form.__dict__.get("errors").setdefault("non_field_error", e)
            return templates.TemplateResponse(form_template, form.__dict__)
    context = {
        "page_header_text": ADMIN_CTYPE_EDIT_HEADER,
        "page_header_help_text": ADMIN_CTYPE_DESCRIPTION,
        "user": user,
    }
    context.update(form.__dict__)
    return templates.TemplateResponse(form_template, context)


@router.get("/{pk}/delete")
async def delete_ctype_admin(
    pk: int, request: Request, user: User = Depends(get_current_admin)
):
    ct = await CarrierTypesServise.get_by_id(pk)

    if not ct:
        return redirect_with_error(request, index_url, "Тип ключевого носителя не найден.")

    carriers = await KeyCarrierServise.all(carrier_type_id=ct.id)

    if carriers:
        versions_names = "; ".join([str(item) for item in carriers])
        return redirect_with_error(
            request,
            index_url,
            f"Невозможно удалить тип ключевого носителя '{ct}', так как от неё зависят версии СКЗИ: {versions_names}"
        )

    try:
        await CarrierTypesServise.delete(pk)
        return redirect_with_message(request, index_url, "Тип ключевого носителя удален!")
    except Exception as e:
        return redirect_with_error(
            request,
            index_url,
            f"Необработанная ошибка удаления типа ключевого носителя '{ct}': {e}"
        )


class CtypeForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict = {}
        self.name: str

    async def load_data(self):
        form = await self.request.form()
        self.name: str = form.get("name")

    async def is_valid(self):
        name_min_length = 3
        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if self.name:
            db_position = await CarrierTypesServise.get_one_or_none(name=self.name)
            if db_position:
                self.errors.setdefault(
                    "name",
                    f"'{self.name}' - Такой тип ключевого носителя уже существует!",
                )
        if not self.errors:
            return True
        return False
