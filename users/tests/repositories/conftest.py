from testcontainers.mongodb import MongoDbContainer
from typing import Generator
from mongoengine import connect, disconnect
import pytest

from webapp.database.repositories.user import UserRepository


@pytest.fixture(scope="session")
def mongo_db_container() -> Generator[str, None, None]:
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo.get_connection_url()

@pytest.fixture(autouse=True)
def mongo_connection(mongo_db_container: str) -> Generator[None, None, None]:
    connect(host=mongo_db_container, alias="default", uuidRepresentation="standard")
    yield
    disconnect()

@pytest.fixture
def user_repository() -> UserRepository:
    return UserRepository()
