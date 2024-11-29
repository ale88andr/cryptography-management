import datetime
from fastapi import APIRouter, Depends, Response, Request, responses, status

from core.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
)
from core.config import templates
from dependencies.auth import get_current_admin, get_current_user
from forms.login import LoginForm
from forms.password_change import ChangePasswordForm
from models.users import User
from schemas.auth import SUserAuth
from services.auth import authenticate_user, create_jwt_token, get_password_hash
from services.users import UsersDAO


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/api/login")
async def user_login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_jwt_token({"sub": str(user.id)})
    response.set_cookie("cryman_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/login")
async def login(response: Response, request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        user = await authenticate_user(form.email, form.password)

        if not user:
            form.__dict__.update("non_field_error", "Некорректные данные аутентификации")
            return templates.TemplateResponse("login.html", form.__dict__)

        response = responses.RedirectResponse(
            "/admin", status_code=status.HTTP_302_FOUND
        )

        if user.is_password_temporary:
            response = responses.RedirectResponse(
                "/auth/change", status_code=status.HTTP_302_FOUND
            )

        access_token = create_jwt_token({"sub": str(user.id)})
        response.set_cookie("cryman_access_token", access_token, httponly=True)
        await UsersDAO.update(
            user.id,
            last_login_at=datetime.datetime.utcnow(),
            last_login_ip=request.client.host,
            last_login_from=request.headers.get('User-agent'),
        )
        return response
    return templates.TemplateResponse("login.html", form.__dict__)


@router.get("/login")
async def login(response: Response, request: Request, msg: str = None):
    return templates.TemplateResponse("login.html", {"request":request, "msg": msg})


@router.get("/change")
async def change(
    response: Response,
    request: Request,
    user: User = Depends(get_current_user),
    msg: str = None
):
    return templates.TemplateResponse(
        "change.html", {"request":request, "msg": msg, "user": user}
    )


@router.post("/change")
async def change_password(
    response: Response,
    request: Request,
    user: User = Depends(get_current_user),
):
    if user:
        form = ChangePasswordForm(request)
        await form.load_data()
        if await form.is_valid():
            await UsersDAO.update(
                user.id,
                hashed_password=get_password_hash(form.password),
                is_password_temporary=False
            )
            user = await authenticate_user(user.email, form.password)
            response = responses.RedirectResponse(
                "/admin", status_code=status.HTTP_302_FOUND
            )
            access_token = create_jwt_token({"sub": str(user.id)})
            response.set_cookie("cryman_access_token", access_token, httponly=True)
            return response
        return templates.TemplateResponse("change.html", form.__dict__)


@router.get("/logout")
async def logout(response: Response):
    response = responses.RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("cryman_access_token")
    return response


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user
