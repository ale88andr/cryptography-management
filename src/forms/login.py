from forms.base import Form


class LoginForm(Form):

    async def is_valid(self):

        if not self.email:
            self.errors.setdefault("email", "Поле должно быть заполнено")

        if not self.password:
            self.errors.setdefault("password", "Поле должно быть заполнено")

        if not self.errors:
            return True

        return False
