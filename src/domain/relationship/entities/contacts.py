import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.domain.relationship.entities.person import Person
from src.domain.relationship.value_objects.contact_type import ContactType

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_TYPES = frozenset({ContactType.PHONE, ContactType.MOBILE, ContactType.WHATSAPP})


class PersonContact(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    contact_id: int | None = None
    cpf: str = Field(min_length=11, max_length=11)
    contact_type: ContactType
    value: str = Field(min_length=1, max_length=255)
    flag_preferred: bool = Field(default=False)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @field_validator("cpf", mode="before")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        return Person.validate_cpf(value)

    @field_validator("value", mode="before")
    @classmethod
    def strip_value(cls, value: str) -> str:
        stripped = str(value).strip()
        if not stripped:
            raise ValueError("Contact value must not be blank")
        return stripped

    @model_validator(mode="after")
    def validate_value_for_type(self) -> "PersonContact":
        if self.contact_type is ContactType.EMAIL:
            email = self.value.lower()
            if not _EMAIL_PATTERN.fullmatch(email):
                raise ValueError("Invalid email")
            self.value = email
            return self
        if self.contact_type in _PHONE_TYPES:
            digits = "".join(char for char in self.value if char.isdigit())
            if len(digits) < 10 or len(digits) > 13:
                raise ValueError("Invalid phone")
            self.value = digits
        return self
