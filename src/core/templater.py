import enum
from dataclasses import dataclass
from datetime import date

from docxtpl import DocxTemplate


class LogbookTemplatesEnum(enum.Enum):
    LOGBOOK = "logbook.docx"
    INSTANCE_LOGBOOK = "instance_logbook.docx"
    HARDWARE_LOGBOOK = "hardware_logbook.docx"
    PERSONAL_LOGBOOK = "personal_logbook.docx"
    C_USERS_LOGBOOK = "cusers.docx"


class DocumentTemplatesEnum(enum.Enum):
    C_INSTALL = "0_act.docx"
    C_REMOVE = "1_act.docx"
    KD_INSTALL = "2_act.docx"

    LOGBOOK = "logbook.docx"
    INSTANCE_LOGBOOK = "instance_logbook.docx"
    HARDWARE_LOGBOOK = "hardware_logbook.docx"
    PERSONAL_LOGBOOK = "personal_logbook.docx"

    APPOINTMENT_ORDER = "appointment.docx"


class RenderTemplate:

    def __init__(self, template, context, output) -> None:
        self._template = template
        self._context = context
        self._output = output
        self._render()

    def _render(self):
        tpl = DocxTemplate(self._template)
        tpl.render(self._context)
        tpl.save(self._output)


@dataclass
class ActDocument:
    action_date: date
    number: str

    performer: str
    performer_position: str

    month: str
    year: int


@dataclass
class CommisionMembersContext:
    head_commision_member: str
    head_commision_member_position: str

    commision_member: str
    commision_member_position: str


@dataclass
class VersionActDocumentContext(ActDocument):
    sender: str

    cryptography_version: str
    cryptography_version_set: str


@dataclass
class InstallVersionActDocumentContext(VersionActDocumentContext):
    reason_num: str
    reason_date: date


@dataclass
class UninstallVersionActDocumentContext(VersionActDocumentContext):
    reason: str

    head_commision_member: str
    head_commision_member_position: str

    commision_member: str
    commision_member_position: str


@dataclass
class InstallKeyActDocumentContext(ActDocument, CommisionMembersContext):
    reason_num: str
    reason_date: date

    owner: str
    owner_full_name: str
    owner_position: str

    cryptography: str

    key_document_serials: str

    location: str
    sticker: str
    equipment: str


@dataclass
class UninstallKeyActDocumentContext(ActDocument, CommisionMembersContext):
    reason_num: str
    reason_date: date

    owner: str
    owner_full_name: str
    owner_position: str
    owner_organisation: str

    cryptography: str

    key_document_serials: str

    location: str
    equipment: str
