from forms.base import Form
from services.key_carrier import KeyCarrierServise


class KeyCarrierForm(Form):

    async def is_valid(self):

        if not self.serial or not len(self.serial) >= self.DEFAULT_MIN_LENGTH:
            self.errors.setdefault(
                "serial",
                f"Поле должно содержать как минимум {self.DEFAULT_MIN_LENGTH} символа!",
            )
        if self.serial:
            is_exists = await KeyCarrierServise.get_one_or_none(serial=self.serial)
            if is_exists:
                self.errors.setdefault(
                    "serial",
                    f"'{self.serial}' - Ключевой носитель с таким серийным номером уже существует!",
                )

        if not self.type_id or not self.type_id.isnumeric() or self.type_id == 0:
            self.errors.setdefault("type_id", self.REQUIRED_ERROR)

        return not bool(self.errors)
