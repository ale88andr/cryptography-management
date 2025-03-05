from forms.base import Form


class CVersionDecommissioningForm(Form):

    async def is_valid(self):

        if not self.action_date:
            self.errors.setdefault("action_date", self.REQUIRED_ERROR)

        if self.is_invalid_id(self.head_commision_member_id):
            self.errors.setdefault("head_commision_member_id", self.REQUIRED_ERROR)

        if self.is_invalid_id(self.commision_member_id):
            self.errors.setdefault("commision_member_id", self.REQUIRED_ERROR)

        if self.is_invalid_id(self.performer_id):
            self.errors.setdefault("performer_id", self.REQUIRED_ERROR)

        if not self.reason:
            self.errors.setdefault("reason", self.REQUIRED_ERROR)

        if not self.action_date:
            self.errors.setdefault("action_date", self.REQUIRED_ERROR)

        if not self.errors:
            return True

        return False
