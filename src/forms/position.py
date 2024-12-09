from forms.base import Form
from services.position import PositionServise


class PositionForm(Form):

    async def is_valid(self):
        name_min_length = 3
        if not self.name or not len(self.name) >= name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )
        if self.name:
            db_position = await PositionServise.get_one_or_none(name=self.name)
            if db_position:
                self.errors.setdefault(
                    "name", f"'{self.name}' - Такая должность уже существует!"
                )

        if not self.errors:
            return True

        return False
