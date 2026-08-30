from decimal import Decimal

from fastapi import HTTPException

from src.ports.driver.for_manage_parts.dto.part_dto import (
    PartCreateDTO,
    PartDTO,
    PartUpdateDTO,
)
from src.ports.driver.for_manage_parts.interfaces.for_manage_part import ForManagePart
from src.ui.rest.routers.parts.part_router import (
    create_part,
    delete_part,
    read_part,
    update_part,
)


def _dto(part_id: int = 1, **overrides) -> PartDTO:
    payload = {
        "part_id": part_id,
        "description": "Filtro de oleo",
        "brand": "Bosch",
        "manufacturer": "Bosch do Brasil",
        "unit_price": Decimal("89.90"),
        "available_quantity": 0,
    }
    payload.update(overrides)
    return PartDTO(**payload)


class _FakeUseCase(ForManagePart):
    def create_part(self, part: PartCreateDTO) -> PartDTO:
        if not part.brand.strip():
            raise ValueError("Value must not be empty")
        return _dto(description=part.description)

    def read_part(self, part_id: int) -> PartDTO:
        if part_id == 99:
            raise ValueError("Part not found")
        return _dto(part_id)

    def update_part(self, part_id: int, part: PartUpdateDTO) -> PartDTO:
        if part_id == 99:
            raise ValueError("Part not found")
        if part.unit_price is not None and part.unit_price < 0:
            raise ValueError("Input should be greater than or equal to 0")
        return _dto(part_id, description=part.description or "Filtro de oleo")

    def delete_part(self, part_id: int) -> dict:
        if part_id == 99:
            raise ValueError("Part not found")
        return {"ok": True}


def _payload(**overrides) -> PartCreateDTO:
    payload = {
        "description": "Filtro de oleo",
        "brand": "Bosch",
        "manufacturer": "Bosch do Brasil",
        "unit_price": Decimal("89.90"),
    }
    payload.update(overrides)
    return PartCreateDTO(**payload)


def test_router_create_delegates_to_port():
    result = create_part(_payload(), use_case=_FakeUseCase())

    assert result.part_id == 1
    assert result.available_quantity == 0


def test_router_create_maps_value_error_to_400():
    try:
        create_part(_payload(brand="   "), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("expected HTTPException")


def test_router_read_maps_value_error_to_404():
    try:
        read_part(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Part not found"
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_maps_missing_part_to_404():
    try:
        update_part(99, PartUpdateDTO(description="Filtro de ar"), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("expected HTTPException")


def test_router_update_maps_invalid_price_to_400():
    try:
        update_part(1, PartUpdateDTO(unit_price=Decimal("-1")), use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("expected HTTPException")


def test_router_delete_maps_value_error_to_404():
    try:
        delete_part(99, use_case=_FakeUseCase())
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("expected HTTPException")
