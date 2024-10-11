from forms.base import Form
from services.c_model import CModelServise


class CModelForm(Form):

    async def is_valid(self):
        name_min_length = 3

        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )

        if self.name and self.is_create:
            is_exists = await CModelServise.get_one_or_none(name=self.name)
            if is_exists:
                self.errors.setdefault(
                    "name", f"'{self.name}' - модель с таким именем уже существует!"
                )

        if (
            not self.manufacturer_id
            or not self.manufacturer_id.isnumeric()
            or int(self.manufacturer_id) == 0
        ):
            self.errors.setdefault("manufacturer_id", self.REQUIRED_ERROR)

        if not self.errors:
            return True

        return False
