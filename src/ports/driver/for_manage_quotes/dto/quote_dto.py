from decimal import Decimal

from pydantic import BaseModel

from src.ports.driver.for_manage_relationship.dto.vehicle_dto import VehicleDTO


class QuoteServiceItemDTO(BaseModel):
    description: str
    price: Decimal


class QuoteProductItemDTO(BaseModel):
    description: str
    quantity: int
    total_amount: Decimal


class QuoteDTO(BaseModel):
    vehicle: VehicleDTO
    services: list[QuoteServiceItemDTO]
    products: list[QuoteProductItemDTO]
    total_amount: Decimal
    estimated_duration_days: int
    notes: str | None = None


class QuoteDecisionDTO(BaseModel):
    approved: bool
