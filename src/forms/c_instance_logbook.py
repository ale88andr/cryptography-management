from forms.base import Form
from services.key_document import KeyDocumentServise


class CInstanceLogbookAdd(Form):

    async def is_valid(self):

        if (
            not self.version_id
            or not self.version_id.isnumeric()
            or int(self.version_id) == 0
        ):
            self.errors.setdefault("version_id", self.REQUIRED_ERROR)

        if (
            not self.equipment_id
            or not self.equipment_id.isnumeric()
            or int(self.equipment_id) == 0
        ):
            self.errors.setdefault("equipment_id", self.REQUIRED_ERROR)

        if (
            not self.responsible_user_id
            or not self.responsible_user_id.isnumeric()
            or int(self.responsible_user_id) == 0
        ):
            self.errors.setdefault("responsible_user_id", self.REQUIRED_ERROR)

        if (
            not self.responsible_user_id
            or not self.responsible_user_id.isnumeric()
            or int(self.responsible_user_id) == 0
        ):
            self.errors.setdefault("responsible_user_id", self.REQUIRED_ERROR)

        if self.is_create and not self.happened_at:
            self.errors.setdefault("happened_at", self.REQUIRED_ERROR)

        if not self.reason:
            self.errors.setdefault("reason", self.REQUIRED_ERROR)

        if not self.reason_date:
            self.errors.setdefault("reason_date", self.REQUIRED_ERROR)

        if (
            not self.head_commision_member_id
            or not self.head_commision_member_id.isnumeric()
            or int(self.head_commision_member_id) == 0
        ):
            self.errors.setdefault("head_commision_member_id", self.REQUIRED_ERROR)

        if (
            not self.commision_member_id
            or not self.commision_member_id.isnumeric()
            or int(self.commision_member_id) == 0
        ):
            self.errors.setdefault("commision_member_id", self.REQUIRED_ERROR)

        if (
            not self.performer_id
            or not self.performer_id.isnumeric()
            or int(self.performer_id) == 0
        ):
            self.errors.setdefault("performer_id", self.REQUIRED_ERROR)

        if self.responsible_user_id in [
            self.head_commision_member_id,
            self.commision_member_id,
            self.performer_id,
        ]:
            self.errors.setdefault(
                "responsible_user_id",
                "Пользователь СКЗИ не может быть в составе комиссии",
            )

        if self.head_commision_member_id in [
            self.commision_member_id,
            self.performer_id,
        ]:
            self.errors.setdefault(
                "head_commision_member_id",
                "Председатель комиссии не может быть указан в комисии повторно!",
            )

        if self.commision_member_id in [
            self.head_commision_member_id,
            self.performer_id,
        ]:
            self.errors.setdefault(
                "commision_member_id",
                "Участник комиссии не может быть указан в комисии повторно!",
            )

        if self.performer_id in [
            self.head_commision_member_id,
            self.commision_member_id,
        ]:
            self.errors.setdefault(
                "performer_id", "Исполнитель не может быть в составе комисии повторно!"
            )

        if self.key_document_is_unexpired == "on":

            if self.key_document_unexpired_serial:
                is_exists = await KeyDocumentServise.get_one_or_none(
                    serial=self.key_document_unexpired_serial
                )
                if is_exists:
                    self.errors.setdefault(
                        "key_document_unexpired_serial",
                        f"Ключевой документ с серийным номером '{self.key_document_unexpired_serial}' уже существует!",
                    )

            if not self.key_document_unexpired_serial:
                self.errors.setdefault(
                    "key_document_unexpired_serial", self.REQUIRED_ERROR
                )

            if (
                not self.key_document_unexpired_carrier_id
                or not self.key_document_unexpired_carrier_id.isnumeric()
                or int(self.key_document_unexpired_carrier_id) == 0
            ):
                self.errors.setdefault(
                    "key_document_unexpired_carrier_id", self.REQUIRED_ERROR
                )

            if not self.key_document_unexpired_received_from:
                self.errors.setdefault(
                    "key_document_unexpired_received_from", self.REQUIRED_ERROR
                )

            if not self.key_document_unexpired_received_at:
                self.errors.setdefault(
                    "key_document_unexpired_received_at", self.REQUIRED_ERROR
                )

        if (
            self.key_document_is_expired == "on"
            and self.key_document_expired_is_new == "True"
        ):

            if self.key_document_expired_serial:
                is_exists = await KeyDocumentServise.get_one_or_none(
                    serial=self.key_document_expired_serial
                )
                if is_exists:
                    self.errors.setdefault(
                        "key_document_expired_serial",
                        f"Ключевой документ с серийным номером '{self.key_document_expired_serial}' уже существует!",
                    )

            if not self.key_document_expired_serial:
                self.errors.setdefault(
                    "key_document_expired_serial", self.REQUIRED_ERROR
                )

            if (
                not self.key_document_expired_carrier_id
                or not self.key_document_expired_carrier_id.isnumeric()
                or int(self.key_document_expired_carrier_id) == 0
            ):
                self.errors.setdefault(
                    "key_document_expired_carrier_id", self.REQUIRED_ERROR
                )

            if not self.key_document_expired_received_from:
                self.errors.setdefault(
                    "key_document_expired_received_from", self.REQUIRED_ERROR
                )

            if not self.key_document_expired_received_at:
                self.errors.setdefault(
                    "key_document_expired_received_at", self.REQUIRED_ERROR
                )

        if (
            self.key_document_is_expired == "on"
            and self.key_document_expired_is_new == "False"
        ):

            if (
                not self.key_document_id
                or not self.key_document_id.isnumeric()
                or int(self.key_document_id) == 0
            ):
                self.errors.setdefault("key_document_id", self.REQUIRED_ERROR)

        if not self.key_document_is_expired and not self.key_document_is_unexpired:
            self.errors.setdefault(
                "key_document",
                "Установка СКЗИ без набора ключей не имеет смысла, укажите хотя бы один ключевой набор!",
            )

        if not self.errors:
            return True

        return False
