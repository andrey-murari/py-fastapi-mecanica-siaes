from typing import Protocol

from src.domain.customers_and_services.relationship.entities.customers import (
    Customer,
)


class CustomerRepository(Protocol):
    def get_by_id(self, customer_id: int) -> Customer | None: ...
