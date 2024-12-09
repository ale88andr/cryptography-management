from forms.base import Form
from services.location import LocationServise


class LocationForm(Form):

    async def is_valid(self):
        if not self.name or not len(self.name) >= self.DEFAULT_MIN_LENGTH:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {self.DEFAULT_MIN_LENGTH} символа!"
            )

        if self.name:
            db_loc = await LocationServise.get_one_or_none(name=self.name)
            if db_loc and db_loc.building_id == int(self.building_id):
                self.errors.setdefault(
                    "name", f"'{self.name}' - Такое рабочее место уже существует!"
                )

        if not self.building_id or not self.building_id.isnumeric() or int(self.building_id) <= 0:
            self.errors.setdefault("building_id", self.REQUIRED_ERROR)

        return not bool(self.errors)
