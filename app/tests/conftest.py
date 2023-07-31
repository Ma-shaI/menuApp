from collections.abc import Generator
from typing import Any

import pytest
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.api.api_v1 import menu
from app.config import settings
from app.database import get_db


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    app = FastAPI()
    app.include_router(menu.router)
    yield app


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()




@pytest.fixture(scope="function")
def client(
    app: FastAPI,
    db_session: SessionTesting,
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        return db_session


    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
