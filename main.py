from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.repository.database import database
from src.services.routers.customers_router import router as customers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(customers_router)
