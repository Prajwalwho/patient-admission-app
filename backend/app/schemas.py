import re
from datetime import date, datetime
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    ConfigDict,
    StrictInt,
    ValidationInfo,
    field_validator,
)

from .constants import DEPARTMENTS, DOCTORS, GENDERS, WARDS

NAME_PATTERN = re.compile(r"^[A-Za-z]+(?: [A-Za-z]+)*$")  # letters, single spaces

ALLOWED = {
    "gender": GENDERS,
    "ward": WARDS,
    "department": DEPARTMENTS,
    "doctor": DOCTORS,
}


def today_ist() -> date:
    """Today's date in India. Render servers run in UTC, so we can't use date.today()."""
    return datetime.now(ZoneInfo("Asia/Kolkata")).date()


class PatientBase(BaseModel):
    name: str
    age: StrictInt
    gender: str
    ward: str
    department: str
    doctor: str
    admission_date: date

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name is required")
        if len(value) > 100:
            raise ValueError("Name must be at most 100 characters")
        if not NAME_PATTERN.match(value):
            raise ValueError("Name must contain letters only")
        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value < 0 or value > 120:
            raise ValueError("Age must be a number between 0 and 120")
        return value

    @field_validator("gender", "ward", "department", "doctor")
    @classmethod
    def validate_select(cls, value: str, info: ValidationInfo) -> str:
        label = info.field_name.capitalize()
        if not value or not value.strip():
            raise ValueError(f"{label} is required")
        if value not in ALLOWED[info.field_name]:
            raise ValueError(
                f"Invalid {info.field_name}. Choose one of: "
                f"{', '.join(ALLOWED[info.field_name])}"
            )
        return value

    @field_validator("admission_date")
    @classmethod
    def validate_admission_date(cls, value: date) -> date:
        if value > today_ist():
            raise ValueError("Admission date cannot be in the future")
        return value


class PatientCreate(PatientBase):
    """Used for POST. Same rules as the base."""


class PatientUpdate(PatientBase):
    """Used for PUT. Full update, so all rules apply again."""


class PatientResponse(BaseModel):
    """What the API returns. from_attributes lets it read SQLAlchemy objects."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    gender: str
    ward: str
    department: str
    doctor: str
    admission_date: date
    status: str