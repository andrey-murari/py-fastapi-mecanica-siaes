from collections.abc import Generator
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

class Base(DeclarativeBase):
    ...

class Database:
    def __init__(self, create_models: bool = False) -> None:
        self.engine = create_engine(os.getenv("ENGINE_URL"), echo=True)
        self.session_local = sessionmaker(bind=self.engine)
        if create_models:
            Base.metadata.create_all(self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        with self.session_local() as session:
            yield session

    def close(self) -> None:
        self.engine.dispose()