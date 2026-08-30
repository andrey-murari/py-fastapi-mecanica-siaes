import pytest

from src.domain.relationship.application.vehicle_use_cases import VehicleUseCases
from src.domain.relationship.value_objects.fuel_type import FuelType
from src.ports.driver.for_manage_relationship.dto import (
    PersonDTO,
    VehicleCreateDTO,
    VehicleUpdateDTO,
)
from tests.unit.fakes.in_memory_storage import InMemoryStorage

PLATE = "ABC1D23"
VALID_CPF = "52998224725"


def _vehicle_payload(**overrides) -> VehicleCreateDTO:
    payload = {
        "person_id": VALID_CPF,
        "model": "Civic",
        "brand": "Honda",
        "manufacture_year": "2020",
        "model_year": "2021",
        "engine": "2.0",
        "fuel_type": FuelType.GASOLINE,
        "plate": PLATE,
        "color": "Prata",
        "description": "Carro do cliente",
    }
    payload.update(overrides)
    return VehicleCreateDTO(**payload)


def _storage_with_customer(flag_customer: bool = True) -> InMemoryStorage:
    storage = InMemoryStorage()
    storage.save_person(
        PersonDTO(
            person_id=VALID_CPF,
            complete_name="Andrey Murari",
            user_id="52998224725",
            user_modification_id=1,
            flag_customer=flag_customer,
        )
    )
    return storage


def test_create_vehicle_requires_existing_person():
    use_case = VehicleUseCases(storage=InMemoryStorage())
    payload = _vehicle_payload()
    with pytest.raises(ValueError, match="Person not found"):
        use_case.create_vehicle(payload)


def test_create_vehicle_requires_customer_flag():
    use_case = VehicleUseCases(storage=_storage_with_customer(flag_customer=False))
    payload = _vehicle_payload()
    with pytest.raises(ValueError, match="Person is not a customer"):
        use_case.create_vehicle(payload)


def test_create_vehicle_does_not_promote_person_to_customer():
    storage = _storage_with_customer(flag_customer=False)
    use_case = VehicleUseCases(storage=storage)
    payload = _vehicle_payload()
    with pytest.raises(ValueError, match="Person is not a customer"):
        use_case.create_vehicle(payload)
    assert storage.get_person(VALID_CPF).flag_customer is False


def test_create_vehicle_saves_owner_and_plate_on_the_same_record():
    storage = _storage_with_customer()
    created = VehicleUseCases(storage=storage).create_vehicle(_vehicle_payload())
    assert created.vehicle_id == 1
    assert created.person_id == VALID_CPF
    assert created.model == "Civic"
    assert created.fuel_type == FuelType.GASOLINE
    assert created.plate == PLATE
    assert created.color == "Prata"


def test_create_vehicle_rejects_duplicate_plate():
    use_case = VehicleUseCases(storage=_storage_with_customer())
    use_case.create_vehicle(_vehicle_payload())
    payload = _vehicle_payload()
    with pytest.raises(ValueError, match="Plate already exists"):
        use_case.create_vehicle(payload)


def test_create_vehicle_normalizes_plate():
    created = VehicleUseCases(storage=_storage_with_customer()).create_vehicle(
        _vehicle_payload(plate="abc1d23")
    )
    assert created.plate == "ABC1D23"


def test_create_vehicle_rejects_invalid_plate():
    use_case = VehicleUseCases(storage=_storage_with_customer())
    payload = _vehicle_payload(plate="INVALID")
    with pytest.raises(ValueError, match="Invalid plate"):
        use_case.create_vehicle(payload)


def test_create_vehicle_rejects_manufacture_year_after_model_year():
    use_case = VehicleUseCases(storage=_storage_with_customer())
    payload = _vehicle_payload(manufacture_year="2022", model_year="2021")
    with pytest.raises(ValueError, match="Manufacture year cannot be after model year"):
        use_case.create_vehicle(payload)


def test_read_vehicle_returns_owner_and_plate():
    use_case = VehicleUseCases(storage=_storage_with_customer())
    created = use_case.create_vehicle(_vehicle_payload())
    found = use_case.read_vehicle(created.vehicle_id)
    assert found.model == "Civic"
    assert found.plate == PLATE
    assert found.person_id == VALID_CPF


def test_read_vehicle_not_found():
    use_case = VehicleUseCases(storage=InMemoryStorage())
    with pytest.raises(ValueError, match="Vehicle not found"):
        use_case.read_vehicle(99)


def test_update_vehicle_changes_model_and_plate():
    use_case = VehicleUseCases(storage=_storage_with_customer())
    created = use_case.create_vehicle(_vehicle_payload())
    updated = use_case.update_vehicle(
        created.vehicle_id,
        VehicleUpdateDTO(model="City", plate="XYZ1A23"),
    )
    assert updated.model == "City"
    assert updated.plate == "XYZ1A23"


def test_update_vehicle_rejects_duplicate_plate():
    use_case = VehicleUseCases(storage=_storage_with_customer())
    first = use_case.create_vehicle(_vehicle_payload())
    use_case.create_vehicle(_vehicle_payload(plate="XYZ1A23"))
    payload = VehicleUpdateDTO(plate="XYZ1A23")
    with pytest.raises(ValueError, match="Plate already exists"):
        use_case.update_vehicle(first.vehicle_id, payload)


def test_delete_vehicle():
    storage = _storage_with_customer()
    use_case = VehicleUseCases(storage=storage)
    created = use_case.create_vehicle(_vehicle_payload())
    assert use_case.delete_vehicle(created.vehicle_id) == {"ok": True}
    assert storage.get_vehicle(created.vehicle_id) is None


def test_find_vehicles_by_person_id():
    use_case = VehicleUseCases(storage=_storage_with_customer())
    use_case.create_vehicle(_vehicle_payload())
    use_case.create_vehicle(_vehicle_payload(plate="XYZ1A23"))
    found = use_case.find_vehicles_by_person_id(VALID_CPF)
    assert {item.plate for item in found} == {"ABC1D23", "XYZ1A23"}


def test_find_vehicles_by_person_id_returns_empty_when_no_vehicles():
    assert VehicleUseCases(storage=_storage_with_customer()).find_vehicles_by_person_id(
        VALID_CPF
    ) == []


def test_find_vehicles_by_person_id_requires_person():
    use_case = VehicleUseCases(storage=InMemoryStorage())
    with pytest.raises(ValueError, match="Person not found"):
        use_case.find_vehicles_by_person_id(VALID_CPF)


def test_find_vehicles_by_person_id_rejects_invalid_person_id():
    use_case = VehicleUseCases(storage=InMemoryStorage())
    with pytest.raises(ValueError, match="Invalid CPF"):
        use_case.find_vehicles_by_person_id("12345678912")
