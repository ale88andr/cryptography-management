import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from api.v1 import department, employee, position, auth, pages, uploader
from admin import department as admin_department
from admin import position as admin_position
from admin import organisation as admin_organisation
from admin import building as admin_building
from admin import location as admin_location
from admin import employee as admin_employee
from admin import carrier_type as admin_carrier_type
from admin import key_carrier as admin_key_carrier
from admin import c_manufacturer as admin_c_manufacturer
from admin import c_model as admin_c_model
from admin import c_version as admin_c_version
from admin import equipment as admin_equipment
from admin import c_logbook as admin_c_logbook
from admin import c_instance_logbook as admin_c_instance_logbook
from admin import key_document as admin_key_document
from admin import dashboard as admin_dashboard
from core import config
from core.exceptions import TokenDoesntExistsException, TokenExpiredException
from core.logger import LOGGING
from db.connection import db


def init_app():
    db.init()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        # Clean up the db connection
        await db.close()

    app = FastAPI(
        # Вывод логов
        debug=True,
        # Конфигурируем название проекта. Оно будет отображаться в документации
        title=config.PROJECT_NAME,
        # Адрес документации в красивом интерфейсе
        docs_url="/api/openapi",
        # Адрес документации в формате OpenAPI
        openapi_url="/api/openapi.json",
        # Можно сразу сделать небольшую оптимизацию сервиса и заменить стандартный
        # JSON-сереализатор на более шуструю версию, написанную на Rust
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    return app


app = init_app()


# Монтироваие статических файлов и медиа
app.mount("/media", StaticFiles(directory="src/media"), "media")
app.mount("/static", StaticFiles(directory="src/static"), "static")

# Подключаем роутер к серверу, указав префикс /v1/{prefix}
# Теги указываем для удобства навигации по документации
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(position.router)
app.include_router(department.router)

# ========= src/api/v1/pages.py =========
app.include_router(pages.router)

# ========= src/api/v1/uploader.py =========
app.include_router(uploader.router)

# ========= Админка =========
app.include_router(admin_position.router)
app.include_router(admin_department.router)
app.include_router(admin_organisation.router)
app.include_router(admin_building.router)
app.include_router(admin_location.router)
app.include_router(admin_employee.router)
app.include_router(admin_carrier_type.router)
app.include_router(admin_key_carrier.router)
app.include_router(admin_key_document.router)
app.include_router(admin_c_manufacturer.router)
app.include_router(admin_c_model.router)
app.include_router(admin_c_version.router)
app.include_router(admin_equipment.router)
app.include_router(admin_c_logbook.router)
app.include_router(admin_c_instance_logbook.router)
app.include_router(admin_dashboard.router)

# ========= Разрешаем CORS запросы из списка config.origins =========
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,  # Cookies
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],  #
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Haders",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.get("/hi/{who}")
def greet(who: str):
    return f"Hello? {who}?"


@app.get("/hi2")
def greet2(who: str):
    return f"Hello? {who}?"


@app.exception_handler(TokenDoesntExistsException)
async def unicorn_exception_handler(
    request: Request,
    exc: TokenDoesntExistsException
):
    return RedirectResponse(
        request.url_for("login"),
        # status_code=exc.status_code
    )


@app.exception_handler(TokenExpiredException)
async def unicorn_exception_handler(
    request: Request,
    exc: TokenExpiredException
):
    redirect_url = request.url_for("login").include_query_params(msg=exc.detail)
    return RedirectResponse(redirect_url)


if __name__ == "__main__":
    # Приложение должно запускаться с помощью команды
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # параметр reload указывает Uvicorn перезапустить веб-сервер,
    # если содержимое файла main.py изменится
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
