import pytest
from pydantic import ValidationError

from src.domain.relationship.entities.vehicle import Vehicle, VehicleCustomer
from src.domain.relationship.value_objects.fuel_type import FuelType


def test_vehicle_rejects_manufacture_year_after_model_year():
    with pytest.raises(ValidationError, match="Manufacture year cannot be after model year"):
        Vehicle(
            model="Civic",
            brand="Honda",
            manufacture_year="2022",
            model_year="2021",
            engine="2.0",
            fuel_type=FuelType.GASOLINE,
        )


def test_vehicle_customer_accepts_old_and_mercosul_plates():
    old = VehicleCustomer(customer_id=1, plate="ABC1234", color="Preto")
    mercosul = VehicleCustomer(customer_id=1, plate="abc1d23", color="Prata")
    assert old.plate == "ABC1234"
    assert mercosul.plate == "ABC1D23"


def test_vehicle_customer_rejects_invalid_plate():
    with pytest.raises(ValidationError, match="Invalid plate"):
        VehicleCustomer(customer_id=1, plate="AB12CDE", color="Preto")
