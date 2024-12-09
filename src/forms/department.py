from forms.base import Form
from services.department import DepartmentServise


class DepartmentForm(Form):

    async def is_valid(self):
        if not self.name or not len(self.name) >= self.DEFAULT_MIN_LENGTH:
            self.errors.setdefault(
                "name", f"Поле должно содержать как минимум {self.DEFAULT_MIN_LENGTH} символа!"
            )

        if self.name:
            existing_dept = await DepartmentServise.get_one_or_none(name=self.name)
            if existing_dept:
                self.errors.setdefault(
                    "name", f"'{self.name}' - Такой отдел уже существует!"
                )

        return not bool(self.errors)
