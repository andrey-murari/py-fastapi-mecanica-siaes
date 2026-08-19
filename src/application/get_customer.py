from typing import Any

from src.domain.customers_and_services.relationship.customer_repository import (
    CustomerRepository,
)


class GetCustomer:
    def __init__(self, customers: CustomerRepository) -> None:
        self._customers = customers

    def execute(self, customer_id: int) -> dict[str, Any]:
        customer = self._customers.get_by_id(customer_id)
        if customer is None:
            return None
        if not customer.flag_active:
            return "Inativo"
        return customer.model_dump()
