from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr

from core.config import settings
from services.users import UsersDAO


pswd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pswd.hash(password)


def verify_password(plain_password, hashed_password):
    return pswd.verify(plain_password, hashed_password)


def create_jwt_token(data: dict) -> str:
    jwt_data = data.copy()
    jwt_expired_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    jwt_data.update({"expired_at": jwt_expired_at.timestamp()})
    ecoded_jwt = jwt.encode(jwt_data, settings.SECRET_KEY, settings.SECRET_ALG)
    return ecoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.get_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password) or user.is_blocked:
        return None
    return user
