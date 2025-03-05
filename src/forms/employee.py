from forms.base import Form


class EmployeeForm(Form):

    async def is_valid(self):
        name_min_length = 2

        if not self.surname:
            self.errors.setdefault("surname", self.REQUIRED_ERROR)

        if self.name and len(self.surname) < name_min_length:
            self.errors.setdefault(
                "surname",
                f"Поле должно содержать как минимум {name_min_length} символа!",
            )

        if not self.name:
            self.errors.setdefault("name", self.REQUIRED_ERROR)

        if self.name and len(self.name) < name_min_length:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {name_min_length} символа!"
            )

        if self.is_invalid_id(self.position_id):
            self.errors.setdefault("position_id", self.REQUIRED_ERROR)

        if self.is_invalid_id(self.department_id):
            self.errors.setdefault("department_id", self.REQUIRED_ERROR)

        if self.is_invalid_id(self.location_id):
            self.errors.setdefault("location_id", self.REQUIRED_ERROR)

        if not self.errors or self.is_worked == "on":
            return True

        return False
