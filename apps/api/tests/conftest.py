from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///./test_relay_console.db"
os.environ["AUTO_MIGRATE_ON_BOOT"] = "true"

from relay_console.api.deps import get_db  # noqa: E402
from relay_console.db.base import Base  # noqa: E402
from relay_console.main import app  # noqa: E402


@pytest.fixture()
def client():
    engine = create_engine("sqlite:///./test_relay_console.db", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
