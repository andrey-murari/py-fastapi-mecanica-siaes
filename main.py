import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from src.adapters.driving.for_get_address.address_webservice_adapter.viacep_adapter import viacep_adapter
from src.adapters.driving.for_managing_tokens.pyjwt_adapter import PyJwtAdapter
from src.adapters.driving.for_storing_data.rdbms_adapter import rdbms_adapter
from src.domain.relationship.application.auth_use_cases import AuthUseCases
from src.domain.relationship.application.customer_use_cases import (
    CustomerUseCases,
)
from src.domain.relationship.application.vehicle_use_cases import VehicleUseCases
from src.ports.driver.for_authenticate.interfaces.for_authenticate import ForAuthenticate
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ports.driver.for_manage_relationship.interfaces.for_manage_vehicle import ForManageVehicle
from src.ui.rest.dependencies import (
    set_for_authenticate,
    set_for_manage_customer,
    set_for_manage_vehicle,
)
from src.ui.rest.routers.auth.auth_router import auth_router
from src.ui.rest.routers.relationship.customer_router import customer_router
from src.ui.rest.routers.relationship.vehicle_router import vehicle_router

load_dotenv()

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


jwt_secret = _require_env("JWT_SECRET")
expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES") or "60")
admin_login = _require_env("ADMIN_LOGIN")
admin_password = _require_env("ADMIN_PASSWORD")

auth_use_cases: ForAuthenticate = AuthUseCases(
    tokens=PyJwtAdapter(secret=jwt_secret, expire_minutes=expire_minutes),
    admin_login=admin_login,
    admin_password=admin_password,
)
set_for_authenticate(auth_use_cases)

customer_use_cases: ForManageCustomer = CustomerUseCases(
    storage=rdbms_adapter,
    address=viacep_adapter,
)
set_for_manage_customer(customer_use_cases)

vehicle_use_cases: ForManageVehicle = VehicleUseCases(storage=rdbms_adapter)
set_for_manage_vehicle(vehicle_use_cases)


@asynccontextmanager
async def lifespan(app: FastAPI):
    rdbms_adapter.create_db_and_tables()
    yield
    rdbms_adapter.close()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(vehicle_router)
