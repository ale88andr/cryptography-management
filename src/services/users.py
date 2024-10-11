from models.users import User
from services.base import BaseRepository


class UsersDAO(BaseRepository):
    model = User
