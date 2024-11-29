import re
from forms.base import Form


class ChangePasswordForm(Form):
    password_pattern = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)(?=.*[!@#$%^&*()\-_=+{};:,<.>].*)[0-9a-zA-Z!@#$%^&*()\-_=+{};:,<.>]{8,}$')

    async def is_valid(self):

        if not self.password:
            self.errors.setdefault("password", self.REQUIRED_ERROR)

        if not self.password_confirm:
            self.errors.setdefault("password_confirm", self.REQUIRED_ERROR)

        if len(self.password) < 8:
            self.errors.setdefault("password", "Пароль должен быть не менее 8 символов")

        if not self.password_pattern.match(self.password):
            self.errors.setdefault("password", "Пароль должен содержать символы a-z, A-Z, 0-9, !@#$%^&*()\-_=+{};:,<.>")

        if self.password != self.password_confirm:
            self.errors.setdefault("password_confirm", "Пароли не совпадают!")
            self.errors.setdefault("password", "Пароли не совпадают!")

        if not self.errors:
            return True

        return False
