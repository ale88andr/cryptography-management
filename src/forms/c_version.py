from forms.base import Form


class CVersionForm(Form):

    async def is_valid(self):

        if not self.version:
            self.errors.setdefault("version", self.REQUIRED_ERROR)

        if self.is_create and self.is_invalid_id(self.model_id):
            self.errors.setdefault("model_id", self.REQUIRED_ERROR)

        if self.is_create and self.is_invalid_id(self.responsible_user_id):
            self.errors.setdefault("responsible_user_id", self.REQUIRED_ERROR)

        if self.is_create and not self.happened_at:
            self.errors.setdefault("happened_at", self.REQUIRED_ERROR)

        if not self.serial:
            self.errors.setdefault("serial", self.REQUIRED_ERROR)

        if not self.dist_num:
            self.errors.setdefault("dist_num", self.REQUIRED_ERROR)

        if not self.received_from:
            self.errors.setdefault("received_from", self.REQUIRED_ERROR)

        if not self.received_num:
            self.errors.setdefault("received_num", self.REQUIRED_ERROR)

        if not self.received_at:
            self.errors.setdefault("received_at", self.REQUIRED_ERROR)

        if not self.errors:
            return True

        return False
