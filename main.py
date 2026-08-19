from typing import Any

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import dotenv, os
dotenv.load_dotenv()
print(os.getenv("ENGINE_URL"))

from src.application.get_customer import GetCustomer
from src.infrastructure.repository.database import get_session
from src.infrastructure.repository.models.customer_repository import (
    SqlCustomerRepository,
)

app = FastAPI()

@app.get("/customers/{customer_id}")
async def get_customer(
    customer_id: int,
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    customer = GetCustomer(SqlCustomerRepository(session)).execute(customer_id)
    return {"customer": f"{customer}"}
