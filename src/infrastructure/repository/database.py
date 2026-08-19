from collections.abc import Generator
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

ENGINE_URL = os.getenv("ENGINE_URL")
engine = create_engine(ENGINE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
