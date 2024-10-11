from forms.base import Form


class DestructionForm(Form):

    async def is_valid(self):

        if not self.action_date:
            self.errors.setdefault("action_date", self.REQUIRED_ERROR)

        if not self.head_commision_member_id or not self.head_commision_member_id.isnumeric() or int(self.head_commision_member_id) == 0:
            self.errors.setdefault("head_commision_member_id", self.REQUIRED_ERROR)

        if not self.commision_member_id or not self.commision_member_id.isnumeric() or int(self.commision_member_id) == 0:
            self.errors.setdefault("commision_member_id", self.REQUIRED_ERROR)

        if not self.performer_id or not self.performer_id.isnumeric() or int(self.performer_id) == 0:
            self.errors.setdefault("performer_id", self.REQUIRED_ERROR)

        if not self.reason:
            self.errors.setdefault("reason", self.REQUIRED_ERROR)

        if self.head_commision_member_id in [self.commision_member_id, self.performer_id]:
            self.errors.setdefault("head_commision_member_id", "Председатель комиссии не может быть указан в комисии повторно!")

        if self.commision_member_id in [self.head_commision_member_id, self.performer_id]:
            self.errors.setdefault("commision_member_id", "Участник комиссии не может быть указан в комисии повторно!")

        if self.performer_id in [self.head_commision_member_id, self.commision_member_id]:
            self.errors.setdefault("performer_id", "Исполнитель не может быть в составе комисии повторно!")

        if not self.errors:
            return True

        return False