from forms.base import Form
from services.equipment import EquipmentServise


class EquipmentForm(Form):

    async def is_valid(self):

        if not self.id:
            self.errors.setdefault("id", self.REQUIRED_ERROR)

        if self.is_create and self.id:
            is_exists = await EquipmentServise.get_one_or_none(id=self.id)
            if is_exists:
                self.errors.setdefault(
                    "id", f"'{self.id}' - инвентарный номер уже существует!"
                )

        if not self.serial:
            self.errors.setdefault("serial", self.REQUIRED_ERROR)

        if self.is_create and self.serial:
            is_exists = await EquipmentServise.get_one_or_none(serial=self.serial)
            if is_exists:
                self.errors.setdefault(
                    "serial", f"'{self.id}' - серийный номер уже существует у оборудования с инв. № '{is_exists.id}'!"
                )

        if not self.errors:
            return True

        return False
