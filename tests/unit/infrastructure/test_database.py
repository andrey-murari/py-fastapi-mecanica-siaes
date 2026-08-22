from src.infrastructure.repository.database import Database
from src.infrastructure.repository.models.addresses_repository import AddressRepository


def test_in_memory_database_creates_tables_and_opens_session():
    db = Database(url="sqlite:///:memory:")
    db.create_db_and_tables()
    sessions = db.get_session()
    session = next(sessions)
    try:
        assert session.get(AddressRepository, "01001000") is None
    finally:
        sessions.close()
    db.close()


def test_database_uses_engine_url_when_provided():
    db = Database(url="sqlite:///:memory:")
    assert db.url == "sqlite:///:memory:"
    db.close()
