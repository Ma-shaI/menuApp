from collections.abc import Generator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.api.api_v1 import api
from app.config import settings
from app.dependiencies import get_db

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    app = FastAPI()
    app.include_router(api.api_router)
    yield app


@pytest.fixture(scope='function')
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(
        app: FastAPI,
        db_session: Session,
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        return db_session

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
