from fastapi import FastAPI
# from domain.repositories.CustomerRepository import Base, User, Address
# from infrastructure.repositories.engine import engine
# from datetime import date
# from sqlalchemy.orm import Session

# with Session(engine) as session:

#     Base.metadata.create_all(engine)

#     spongebob = User(
#         name="spongebob",
#         fullname="Spongebob Squarepants",
#         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#     )
#     sandy = User(
#         name="sandy",
#         fullname="Sandy Cheeks",
#         addresses=[
#             Address(email_address="sandy@sqlalchemy.org"),
#             Address(email_address="sandy@squirrelpower.org"),
#         ],
#     )
#     patrick = User(name="patrick", fullname="Patrick Star")
#     session.add_all([spongebob, sandy, patrick])
#     session.commit()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}