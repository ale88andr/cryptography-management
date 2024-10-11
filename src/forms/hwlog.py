from forms.base import Form


class HWLogbookForm(Form):

    async def is_valid(self):

        if not self.happened_at:
            self.errors.setdefault("happened_at", self.REQUIRED_ERROR)

        if self.is_invalid_id(self.cryptography_version_id):
            self.errors.setdefault("cryptography_version_id", self.REQUIRED_ERROR)

        if not self.record_type.isnumeric() or int(self.record_type) < 0:
            self.errors.setdefault("record_type", self.REQUIRED_ERROR)
        elif int(self.record_type) not in [2, 5, 6, 7]:
            self.errors.setdefault(
                "record_type", "Этот тип события недоступен для ручного ввода!"
            )

        if not self.errors:
            return True

        return False
