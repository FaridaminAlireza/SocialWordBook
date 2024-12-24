import logging
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.database import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


logging.basicConfig()
logging.getLogger("sqlalchemy").setLevel(logging.INFO)


@pytest.fixture(scope="module")
def db_session():
    """Create a new database session for a test."""
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Drop tables after the test


# Override the get_db dependency in tests
@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, db_session):
    def _get_test_db():
        yield db_session

    monkeypatch.setattr("configs.database.get_db", _get_test_db)
