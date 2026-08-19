from src.domain.customers_and_services.relationship.entities import Customer
from typing import Any

class CustomerManager:
    def __init__(self):
        ...

    def create_customer(self, customer: dict[str, Any]) -> Customer:
        return Customer(
            customer_id=customer["customer_id"],
            people=customer["people"],
            flag_active=customer["flag_active"],
            insertion_date=customer["insertion_date"]
        )

    def update_customer(self) -> Customer:
        ...

    def delete_customer(self) -> Customer:
        ...

    def get_customer_by_id(self, id: int) -> Customer:
        ...