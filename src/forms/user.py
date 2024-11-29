import re
from forms.base import Form


class UserForm(Form):

    async def is_valid(self):
        email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not self.email:
            self.errors.setdefault("email", self.REQUIRED_ERROR)

        if not email_pattern.match(self.email):
            self.errors.setdefault("email", "Email не корректен!")

        if not self.errors:
            return True

        return False
