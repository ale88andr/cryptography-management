from fastapi import Request


class Form:
    REQUIRED_ERROR = "Поле должно быть заполнено!"

    def __init__(self, request: Request, is_create: bool = True):
        self.request: Request = request
        self.errors: dict = {}
        self.fields: dict = {}
        self.is_create: bool = is_create

    async def load_data(self):
        self.fields = await self.request.form()

    def is_valid_id(self, value) -> bool:
        if value:
            if value.isnumeric():
                return int(value) > 0
        return False

    def is_invalid_id(self, value):
        return not self.is_valid_id(value)

    def __getattr__(self, __name: str):
        if __name in ['request', 'errors', 'fields', 'is_create']:
            return super().__getattribute__(__name)

        return self.fields.get(__name)
