from decimal import Decimal

import pytest

from src.domain.services.application.service_use_cases import ServiceUseCases
from src.ports.driver.for_manage_services.dto.service_dto import (
    ServiceCreateDTO,
    ServiceUpdateDTO,
)
from tests.unit.fakes.in_memory_storage import InMemoryStorage


def _use_cases() -> tuple[ServiceUseCases, InMemoryStorage]:
    storage = InMemoryStorage()
    return ServiceUseCases(storage=storage), storage


def test_create_service_persists_with_defaults():
    use_cases, storage = _use_cases()

    created = use_cases.create_service(
        ServiceCreateDTO(description="Troca de oleo", price=Decimal("150.00"))
    )

    assert created.service_id == 1
    assert created.flag_active is True
    assert created.average_duration_minutes == 60
    assert storage.get_service(1) is not None


def test_create_service_trims_description():
    use_cases, _ = _use_cases()

    created = use_cases.create_service(
        ServiceCreateDTO(description="  Alinhamento  ", price=Decimal("80.00"))
    )

    assert created.description == "Alinhamento"


def test_create_service_rejects_short_description():
    use_cases, _ = _use_cases()

    payload = ServiceCreateDTO(description="ab", price=Decimal("10.00"))
    with pytest.raises(ValueError):
        use_cases.create_service(payload)


def test_create_service_rejects_negative_price():
    use_cases, _ = _use_cases()

    payload = ServiceCreateDTO(description="Troca de oleo", price=Decimal("-1.00"))
    with pytest.raises(ValueError):
        use_cases.create_service(payload)


def test_read_service_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Service not found"):
        use_cases.read_service(1)


def test_update_service_changes_price():
    use_cases, _ = _use_cases()
    created = use_cases.create_service(
        ServiceCreateDTO(description="Troca de oleo", price=Decimal("150.00"))
    )

    updated = use_cases.update_service(
        created.service_id, ServiceUpdateDTO(price=Decimal("200.00"))
    )

    assert updated.price == Decimal("200.00")
    assert updated.description == "Troca de oleo"


def test_update_service_rejects_invalid_price():
    use_cases, _ = _use_cases()
    created = use_cases.create_service(
        ServiceCreateDTO(description="Troca de oleo", price=Decimal("150.00"))
    )

    payload = ServiceUpdateDTO(price=Decimal("-5.00"))
    with pytest.raises(ValueError):
        use_cases.update_service(created.service_id, payload)


def test_delete_service_removes_it():
    use_cases, storage = _use_cases()
    created = use_cases.create_service(
        ServiceCreateDTO(description="Troca de oleo", price=Decimal("150.00"))
    )

    assert use_cases.delete_service(created.service_id) == {"ok": True}
    assert storage.get_service(created.service_id) is None


def test_delete_service_not_found():
    use_cases, _ = _use_cases()

    with pytest.raises(ValueError, match="Service not found"):
        use_cases.delete_service(42)
