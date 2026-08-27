from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.domain.relationship.value_objects.fuel_type import FuelType

_PLATE_PATTERN = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")


class Vehicle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle_id: int | None = None
    model: str = Field(min_length=1, max_length=100)
    brand: str = Field(min_length=1, max_length=50)
    manufacture_year: str = Field(min_length=4, max_length=4)
    model_year: str = Field(min_length=4, max_length=4)
    engine: str = Field(min_length=1, max_length=50)
    fuel_type: FuelType
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @field_validator("manufacture_year", "model_year", mode="before")
    @classmethod
    def validate_year(cls, value: str) -> str:
        year = str(value)
        if not year.isdigit() or len(year) != 4:
            raise ValueError("Year must contain exactly 4 digits")
        year_number = int(year)
        current_year = datetime.now().year
        if year_number < 1900 or year_number > current_year + 1:
            raise ValueError("Year is out of range")
        return year

    @model_validator(mode="after")
    def validate_year_order(self) -> "Vehicle":
        if int(self.manufacture_year) > int(self.model_year):
            raise ValueError("Manufacture year cannot be after model year")
        return self


class VehicleCustomer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle_customer_id: int | None = None
    vehicle_id: int | None = None
    customer_id: int = Field(gt=0)
    plate: str = Field(min_length=7, max_length=7)
    color: str = Field(min_length=3, max_length=20)
    description: str | None = Field(default=None, max_length=255)
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None

    @field_validator("plate", mode="before")
    @classmethod
    def validate_plate(cls, value: str) -> str:
        plate = "".join(char for char in str(value).upper() if char.isalnum())
        if not _PLATE_PATTERN.fullmatch(plate):
            raise ValueError("Invalid plate")
        return plate
