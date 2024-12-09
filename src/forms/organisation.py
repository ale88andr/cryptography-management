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

        return not bool(self.errors)
