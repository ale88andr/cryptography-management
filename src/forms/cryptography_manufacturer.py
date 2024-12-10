from forms.base import Form
from services.c_manufacturer import CManufacturerServise


class CryptographyManufacturerForm(Form):

    async def is_valid(self):
        if not self.name or not len(self.name) >= self.DEFAULT_MIN_LENGTH:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {self.DEFAULT_MIN_LENGTH} символа!"
            )

        if self.name:
            manufacturer = await CManufacturerServise.get_one_or_none(name=self.name)
            if manufacturer:
                self.errors.setdefault(
                    "name",
                    f"'{self.name}' - Производитель с таким именем уже существует!",
                )

        return not bool(self.errors)
