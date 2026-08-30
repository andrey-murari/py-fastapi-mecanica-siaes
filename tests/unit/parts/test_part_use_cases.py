from decimal import Decimal

import pytest

from src.domain.inventory.application.parts_use_cases import PartUseCases
from src.ports.driver.for_manage_parts.dto.part_dto import PartCreateDTO, PartUpdateDTO
from tests.unit.fakes.in_memory_storage import InMemoryStorage


def _use_cases() -> tuple[PartUseCases, InMemoryStorage]:
    storage = InMemoryStorage()
    return PartUseCases(storage=storage), storage


def _payload(**overrides) -> PartCreateDTO:
    payload = {
        "description": "Filtro de oleo",
        "brand": "Bosch",
        "manufacturer": "Bosch do Brasil",
        "unit_price": Decimal("89.90"),
    }
    payload.update(overrides)
    return PartCreateDTO(**payload)


def test_create_part_persists_with_zero_stock():
    use_cases, storage = _use_cases()

    created = use_cases.create_part(_payload())

    assert created.part_id == 1
    assert created.available_quantity == 0
    assert created.flag_active is True
    assert storage.get_part(1) is not None


def test_create_part_rejects_blank_brand():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError):
        use_cases.create_part(_payload(brand="   "))


def test_read_part_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Part not found"):
        use_cases.read_part(1)


def test_update_part_changes_description():
    use_cases, _ = _use_cases()
    created = use_cases.create_part(_payload())

    updated = use_cases.update_part(created.part_id, PartUpdateDTO(description="Filtro de ar"))

    assert updated.description == "Filtro de ar"
    assert updated.available_quantity == 0


def test_update_part_rejects_negative_price():
    use_cases, _ = _use_cases()
    created = use_cases.create_part(_payload())

    with pytest.raises(ValueError):
        use_cases.update_part(created.part_id, PartUpdateDTO(unit_price=Decimal("-1")))


def test_delete_part_removes_it():
    use_cases, storage = _use_cases()
    created = use_cases.create_part(_payload())

    assert use_cases.delete_part(created.part_id) == {"ok": True}
    assert storage.get_part(created.part_id) is None


def test_delete_part_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Part not found"):
        use_cases.delete_part(7)
