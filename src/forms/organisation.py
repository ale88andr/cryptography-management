from forms.base import Form


class OrganisationForm(Form):

    async def is_valid(self):
        if not self.name or not len(self.name) >= self.DEFAULT_MIN_LENGTH:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {self.DEFAULT_MIN_LENGTH} символа!"
            )

        if not self.short_name or not len(self.short_name) >= self.DEFAULT_MIN_LENGTH:
            self.errors.setdefault(
                "short_name",
                f"Поле должно содержать как минимум {self.DEFAULT_MIN_LENGTH} символа!",
            )

        if not self.city:
            self.errors.setdefault("city", self.REQUIRED_ERROR)

        if not self.building:
            self.errors.setdefault("building", self.REQUIRED_ERROR)

        if not self.chief:
            self.errors.setdefault("chief", self.REQUIRED_ERROR)

        if self.index and not self.index.isnumeric():
            self.errors.setdefault("index", self.NON_NUMERIC_ERROR)

        self.chief_id = None if not self.chief_id or self.chief_id == '0' else int(self.chief_id)
        self.responsible_employee_id = None if not self.responsible_employee_id or self.responsible_employee_id == '0' else int(self.responsible_employee_id)
        self.spare_responsible_employee_id = None if not self.spare_responsible_employee_id or self.spare_responsible_employee_id == '0' else int(self.spare_responsible_employee_id)

        if not self.chief_id:
            self.errors.setdefault("chief_id", self.REQUIRED_ERROR)

        if self.responsible_employee_id and self.responsible_employee_id == self.spare_responsible_employee_id:
            err_msg = "Не может быть одно и то же лицо"
            self.errors.setdefault("responsible_employee_id", err_msg)
            self.errors.setdefault("spare_responsible_employee_id", err_msg)

        return not bool(self.errors)
