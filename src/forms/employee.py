from forms.base import Form


class EmployeeForm(Form):

    async def is_valid(self):
        name_min_length = 2

        if not self.surname:
            self.errors.setdefault("surname", self.REQUIRED_ERROR)

        if len(self.surname) < name_min_length:
            self.errors.setdefault(
                "surname",
                f"Поле должно содержать как минимум {name_min_length} символа!",
            )

        if not self.name:
            self.errors.setdefault("name", self.REQUIRED_ERROR)

        if len(self.name) < name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )

        if (
            not self.position_id
            or not self.position_id.isnumeric()
            or int(self.position_id) == 0
        ):
            self.errors.setdefault("position_id", self.REQUIRED_ERROR)

        if (
            not self.department_id
            or not self.department_id.isnumeric()
            or int(self.department_id) == 0
        ):
            self.errors.setdefault("department_id", self.REQUIRED_ERROR)

        if (
            not self.location_id
            or not self.location_id.isnumeric()
            or int(self.location_id) == 0
        ):
            self.errors.setdefault("location_id", self.REQUIRED_ERROR)

        if not self.errors:
            return True

        return False
