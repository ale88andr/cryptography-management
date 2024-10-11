from fastapi import APIRouter, Depends, Response

from core.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from dependencies.auth import get_current_admin, get_current_user
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
    await UsersDAO.create(
        email=user_data.email, hashed_password=hashed_password
    )


@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_jwt_token({"sub": str(user.id)})
    response.set_cookie("cryman_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("cryman_access_token")


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user


@router.get("/all")
async def all_users(user: User = Depends(get_current_admin)):
    return await UsersDAO.get_all()
