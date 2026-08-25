from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.driving.for_get_address.address_webservice_adapter.viacep_adapter import (
    viacep_adapter,
)
from src.adapters.driving.for_storing_data.rdbms_adapter import rdbms_adapter
from src.domain.relationship.application.customer_use_cases import (
    CustomerUseCases,
)
from src.ports.driver.for_manage_relationship.interfaces.for_manage_customer import ForManageCustomer
from src.ui.rest.dependencies import set_for_manage_customer
from src.ui.rest.routers.relationship.customer_router import customer_router

customer_use_cases: ForManageCustomer = CustomerUseCases(
    storage=rdbms_adapter,
    address=viacep_adapter,
)
set_for_manage_customer(customer_use_cases)


@asynccontextmanager
async def lifespan(app: FastAPI):
    rdbms_adapter.create_db_and_tables()
    yield
    rdbms_adapter.close()


app = FastAPI(lifespan=lifespan)
app.include_router(customer_router)
