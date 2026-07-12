from fastapi import FastAPI
from domain.entities.customer import Customer
from datetime import date


app = FastAPI()

@app.get("/")
async def root():
    return None