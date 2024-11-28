from datetime import datetime
from fastapi import Depends, Request
from jose import jwt, JWTError

from core.config import settings
from core.exceptions import (
    IncorrectTokenException,
    TokenDoesntExistsException,
    TokenExpiredException,
    UserActionForbiddenException,
    UserDoesntExistsException,
)
from services.users import UsersDAO
from models.users import User


def get_token(request: Request):
    token = request.cookies.get("cryman_access_token")
    if not token:
        raise TokenDoesntExistsException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.SECRET_ALG)
    except JWTError as e:
        raise IncorrectTokenException from e

    expired_at: str = payload.get("expired_at")

    if not expired_at or (int(expired_at) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")

    if not user_id:
        raise UserDoesntExistsException

    user = await UsersDAO.get_by_id(int(user_id))

    if not user:
        raise UserDoesntExistsException

    return user


async def get_current_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise UserActionForbiddenException
    return user
