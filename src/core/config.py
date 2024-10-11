import os
import locale
from logging import config as logging_config
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings

from core.logger import LOGGING


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_ENGINE: str
    SECRET_KEY: str
    SECRET_ALG: str

    @property
    def db_connection_string(self) -> str:
        return (f"{self.DB_ENGINE}://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    class Config:
        env_file = ".env"


settings = Settings()

# Настройки логгирования
logging_config.dictConfig(LOGGING)

# Название проекта. Для Swagger-документации
PROJECT_NAME = os.getenv("PROJECT_NAME", "Cryptography Management")

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Домены CORS
origins = [
    "http://localhost:3000",
]

# Настройка поиска шаблонов Jinja
templates = Jinja2Templates(directory="src/templates")

# Настройка локали
locale.setlocale(category=locale.LC_ALL,locale="ru_RU.UTF-8")
