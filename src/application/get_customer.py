from typing import Any

from src.domain.customers_and_services.relationship.customer_repository import (
    CustomerRepository,
)
from src.domain.customers_and_services.relationship.entities.customers import (
    Customer,
)


class GetCustomer:
    def __init__(self, customers: CustomerRepository) -> None:
        self._customers = customers

    def execute(self, customer_id: int) -> dict[str, Any] | str | None:
        customer = self._customers.get_by_id(customer_id)
        if customer is None:
            return None
        if not customer.flag_active:
            return "Inativo"
        return customer.model_dump()


class SaveCustomer:
    def __init__(self, customers: CustomerRepository) -> None:
        self._customers = customers

    def execute(self, customer: Customer) -> dict[str, Any]:
        saved = self._customers.save(customer)
        return saved.model_dump()
