from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.relationship.value_objects.fuel_type import FuelType


class VehicleDTO(BaseModel):
    vehicle_id: int = Field(gt=0)
    model: str = Field(min_length=7, max_length=7)
    brand: str = Field(min_length=3, max_length=20)
    year: int = Field(gt=0)
    fuel_type: FuelType = Field(min_length=3, max_length=20)
    engine_capacity: float = Field(gt=0)
    user_modification_id: int = Field(gt=0)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = Field(default=None)


class VehicleCustomerDTO(BaseModel):
    vehicle_id: int = Field(gt=0)
    vehicle_customer_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    plate: str = Field(min_length=7, max_length=7)
    color: str = Field(min_length=3, max_length=20)
    description: str = Field(min_length=3, max_length=255)
    user_modification_id: int = Field(gt=0)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime | None = Field(default=None)

class VehicleCreateDTO(BaseModel):
    vehicle_id: int = Field(gt=0)
    model: str = Field(min_length=7, max_length=7)
    brand: str = Field(min_length=3, max_length=20)
    year: int = Field(gt=0)
    fuel_type: FuelType = Field(min_length=3, max_length=20)
    engine_capacity: float = Field(gt=0)
    user_modification_id: int = Field(gt=0)
    flag_active: bool = Field(default=True)
    insertion_date: datetime = Field(default_factory=datetime.now)
    modification_date: datetime = Field(default_factory=datetime.now)

class VehicleUpdateDTO(BaseModel):
    model: str | None = Field(min_length=7, max_length=7)
    brand: str | None = Field(min_length=3, max_length=20)
    year: int | None = Field(gt=0)
    fuel_type: FuelType | None = Field(min_length=3, max_length=20)
    engine_capacity: float | None = Field(gt=0)
    user_modification_id: int | None = Field(gt=0)
    flag_active: bool | None = Field(default=True)
    modification_date: datetime | None = Field(default_factory=datetime.now)