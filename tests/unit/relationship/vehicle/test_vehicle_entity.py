import pytest
from pydantic import ValidationError

from src.domain.relationship.entities.vehicle import Vehicle
from src.domain.relationship.value_objects.fuel_type import FuelType

VALID_CPF = "52998224725"


def _vehicle(**overrides) -> Vehicle:
    payload = {
        "person_id": VALID_CPF,
        "model": "Civic",
        "brand": "Honda",
        "manufacture_year": "2020",
        "model_year": "2021",
        "engine": "2.0",
        "fuel_type": FuelType.GASOLINE,
        "plate": "ABC1D23",
        "color": "Preto",
    }
    payload.update(overrides)
    return Vehicle(**payload)


def test_vehicle_rejects_manufacture_year_after_model_year():
    with pytest.raises(ValidationError, match="Manufacture year cannot be after model year"):
        _vehicle(manufacture_year="2022", model_year="2021")


def test_vehicle_accepts_old_and_mercosul_plates():
    assert _vehicle(plate="ABC1234").plate == "ABC1234"
    assert _vehicle(plate="abc1d23").plate == "ABC1D23"


def test_vehicle_rejects_invalid_plate():
    with pytest.raises(ValidationError, match="Invalid plate"):
        _vehicle(plate="AB12CDE")


def test_vehicle_accepts_cnpj_owner():
    assert _vehicle(person_id="11.222.333/0001-81").person_id == "11222333000181"


def test_vehicle_rejects_invalid_person_id():
    with pytest.raises(ValidationError, match="Invalid CPF"):
        _vehicle(person_id="12345678912")
