import re
from forms.base import Form
from services.users import UsersDAO


class UserForm(Form):

    async def is_valid(self):
        email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        existing_user = await UsersDAO.get_one_or_none(email=self.email)

        if not self.email:
            self.errors.setdefault("email", self.REQUIRED_ERROR)

        if not email_pattern.match(self.email):
            self.errors.setdefault("email", "Email не корректен!")

        if self.is_create and existing_user:
            self.errors.setdefault("email", "Пользователь с таким email уже существует!")

        if self.is_create and not self.password:
            self.errors.setdefault("password", self.REQUIRED_ERROR)

        if not self.errors:
            return True

        return False
