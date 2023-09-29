import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.main import create_app
from src.core.config import settings

engine_url = settings.DATABASE_URL
_db_conn = create_engine(engine_url)


@pytest.fixture()
def test_db_session():
    session = Session(bind=_db_conn)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def test_app() -> TestClient:
    with TestClient(app=create_app()) as client:
        yield client
