from collections.abc import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DEFAULT_SQLITE_URL = "sqlite:///database.db"


class Base(DeclarativeBase):
    ...


def _connect_args(url: str) -> dict:
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


class Database:
    def __init__(
        self,
        url: str | None = None,
        create_models: bool = False,
        echo: bool = False,
    ) -> None:
        self.url = url or os.getenv("ENGINE_URL") or DEFAULT_SQLITE_URL
        self.engine = create_engine(
            self.url,
            echo=echo,
            connect_args=_connect_args(self.url),
        )
        self.session_local = sessionmaker(bind=self.engine, class_=Session)
        if create_models:
            self.create_db_and_tables()

    def create_db_and_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        with self.session_local() as session:
            yield session

    def close(self) -> None:
        self.engine.dispose()


database = Database(url=DEFAULT_SQLITE_URL)
