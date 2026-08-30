import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from src.adapters.driving.for_get_address.address_webservice_adapter.viacep_adapter import viacep_adapter
from src.adapters.driving.for_managing_tokens.pyjwt_adapter import PyJwtAdapter
from src.adapters.driving.for_storing_data.rdbms_adapter import rdbms_adapter

from src.domain.inventory.application.inventory_use_cases import InventoryUseCases
from src.domain.relationship.application.auth_use_cases import AuthUseCases
from src.domain.relationship.application.customer_use_cases import CustomerUseCases
from src.domain.order_services.application.order_use_cases import ServiceOrderUseCases
from src.domain.order_services.application.quote_use_cases import QuoteUseCases
from src.domain.inventory.application.parts_use_cases import PartUseCases
from src.domain.relationship.application.person_use_cases import PersonUseCases
from src.domain.relationship.application.user_use_cases import UserUseCases
from src.domain.relationship.application.vehicle_use_cases import VehicleUseCases
from src.domain.services.application.service_use_cases import ServiceUseCases

from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ports.driver.for_manage_inventory.interfaces.for_manage_inventory import (
    ForManageInventory,
)
from src.ports.driver.for_manage_parts.interfaces.for_manage_part import ForManagePart
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ports.driver.for_manage_relationship.interfaces.for_manage_person import ForManagePerson
from src.ports.driver.for_manage_relationship.interfaces.for_manage_user import ForManageUser
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ports.driver.for_manage_quotes.interfaces.for_manage_quote import ForManageQuote
from src.ports.driver.for_manage_service_orders.interfaces.for_manage_service_order import ForManageServiceOrder
from src.ports.driver.for_manage_services.interfaces.for_manage_service import ForManageService

from src.ui.rest.dependencies import (
    set_for_authenticate,
    set_for_manage_customer,
    set_for_manage_inventory,
    set_for_manage_part,
    set_for_manage_person,
    set_for_manage_user,
    set_for_manage_service,
    set_for_manage_quote,
    set_for_manage_service_order,
    set_for_manage_vehicle,
)

from src.ui.rest.routers.auth.auth_router import auth_router
from src.ui.rest.routers.inventory.inventory_router import inventory_router
from src.ui.rest.routers.parts.part_router import part_router
from src.ui.rest.routers.relationship.customer_router import customer_router
from src.ui.rest.routers.relationship.person_router import person_router
from src.ui.rest.routers.relationship.user_router import user_router
from src.ui.rest.routers.relationship.vehicle_router import vehicle_router
from src.ui.rest.routers.service_orders.quote_router import quote_router
from src.ui.rest.routers.service_orders.service_order_router import service_order_router
from src.ui.rest.routers.services.service_router import service_router

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


jwt_secret = _require_env("JWT_SECRET")
expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES") or "60")
admin_login = _require_env("ADMIN_LOGIN")
admin_password = _require_env("ADMIN_PASSWORD")

auth_use_cases: ForAuthenticate = AuthUseCases(tokens=PyJwtAdapter(secret=jwt_secret, expire_minutes=expire_minutes), admin_login=admin_login, admin_password=admin_password)
customer_use_cases: ForManageCustomer = CustomerUseCases(storage=rdbms_adapter, address=viacep_adapter)
person_use_cases: ForManagePerson = PersonUseCases(storage=rdbms_adapter)
user_use_cases: ForManageUser = UserUseCases(storage=rdbms_adapter)
vehicle_use_cases: ForManageVehicle = VehicleUseCases(storage=rdbms_adapter)
service_use_cases: ForManageService = ServiceUseCases(storage=rdbms_adapter)
part_use_cases: ForManagePart = PartUseCases(storage=rdbms_adapter)
inventory_use_cases: ForManageInventory = InventoryUseCases(storage=rdbms_adapter)
service_order_use_cases: ForManageServiceOrder = ServiceOrderUseCases(
    storage=rdbms_adapter,
    inventory=inventory_use_cases,
    services=service_use_cases,
)
quote_use_cases: ForManageQuote = QuoteUseCases(
    storage=rdbms_adapter,
    inventory=inventory_use_cases,
)

set_for_authenticate(auth_use_cases)
set_for_manage_customer(customer_use_cases)
set_for_manage_person(person_use_cases)
set_for_manage_user(user_use_cases)
set_for_manage_vehicle(vehicle_use_cases)
set_for_manage_service(service_use_cases)
set_for_manage_part(part_use_cases)
set_for_manage_inventory(inventory_use_cases)
set_for_manage_service_order(service_order_use_cases)
set_for_manage_quote(quote_use_cases)


@asynccontextmanager
async def lifespan(app: FastAPI):
    rdbms_adapter.create_db_and_tables()
    yield
    rdbms_adapter.close()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(person_router)
app.include_router(user_router)
app.include_router(vehicle_router)
app.include_router(service_router)
app.include_router(part_router)
app.include_router(inventory_router)
app.include_router(service_order_router)
app.include_router(quote_router)
