from fastapi import HTTPException, status


class CustomHTTPException(
    HTTPException
):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(
    CustomHTTPException
):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(
    CustomHTTPException
):  # <-- обязательно наследуемся от нашего класса
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная данные аутентификации"


class TokenExpiredException(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек! Требуется повторная аутентификация."


class TokenDoesntExistsException(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен пользователя не найден"


class IncorrectTokenException(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserDoesntExistsException(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserActionForbiddenException(CustomHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Пользователь не имеет полномочий на это действие"


class UserAddException(CustomHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь не добавлен"


class LogbookOnDeleteException(CustomHTTPException):
    status_code = status.HTTP_303_SEE_OTHER
    detail = "Данное СКЗИ зарегистрированно в журнале учёта, удалите запись из журнала!"
