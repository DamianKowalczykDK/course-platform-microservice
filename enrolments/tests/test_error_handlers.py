from webapp.services.exceptions import  ServiceException, ValidationException
from webapp import register_error_handlers
from flask.typing import ResponseReturnValue
from flask.testing import FlaskClient
from flask import Flask
from typing import Generator
from pydantic import BaseModel
import pytest

class TestAgeSchema(BaseModel):
    age: int


@pytest.fixture
def app_with_error_handlers() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    register_error_handlers(app)

    @app.route("/boom")
    def boom() -> ResponseReturnValue:
        raise RuntimeError("Boom")

    @app.route("/apiexception")
    def api_exception() -> ResponseReturnValue:
        raise ServiceException()

    @app.route("/validation")
    def validation() -> ResponseReturnValue:
        TestAgeSchema.model_validate({"age": "bad"})
        raise ValidationException()

    yield app

@pytest.fixture
def client(app_with_error_handlers: Flask) -> FlaskClient:
    return app_with_error_handlers.test_client()

def test_not_found(client: FlaskClient) -> None:
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_server_error(client: FlaskClient) -> None:
    response = client.get("/boom")
    assert response.status_code == 500

def test_validation_pydantic(client: FlaskClient) -> None:
    response = client.get("/validation")
    assert response.status_code == 400

def test_api_exception(client: FlaskClient) -> None:
    response = client.get("/apiexception")
    assert response.status_code == 500

    data = response.get_json()
    assert data["message"] == "Service error"