from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.domain.relationship.value_objects.fuel_type import FuelType


class VehicleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle_id: int | None = None
    person_id: str
    model: str
    brand: str
    manufacture_year: str
    model_year: str
    engine: str
    fuel_type: FuelType
    plate: str
    color: str
    description: str | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = None


class VehicleCreateDTO(BaseModel):
    person_id: str = Field(examples=["52998224725"])
    model: str = Field(examples=["Civic"])
    brand: str = Field(examples=["Honda"])
    manufacture_year: str = Field(examples=["2020"])
    model_year: str = Field(examples=["2021"])
    engine: str = Field(examples=["2.0"])
    fuel_type: FuelType
    plate: str = Field(examples=["ABC1D23"])
    color: str = Field(examples=["Preto"])
    description: str | None = None
    user_modification_id: int = Field(default=1)
    flag_active: bool = True


class VehicleUpdateDTO(BaseModel):
    model: str | None = None
    brand: str | None = None
    manufacture_year: str | None = None
    model_year: str | None = None
    engine: str | None = None
    fuel_type: FuelType | None = None
    plate: str | None = None
    color: str | None = None
    description: str | None = None
    flag_active: bool | None = None
