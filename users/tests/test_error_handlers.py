from webapp.services.exceptions import ServerException, ValidationException
from webapp import register_error_handlers
from flask.typing import ResponseReturnValue
from flask.testing import FlaskClient
from flask import Flask
from pydantic import BaseModel
from typing import Generator
import pytest

class AgeSchema(BaseModel):
    age: int

@pytest.fixture()
def app_with_handlers() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    register_error_handlers(app)

    @app.route("/boom")#type: ignore
    def boom() -> ResponseReturnValue:
        raise RuntimeError("BOOM!")

    @app.route("/apiexception")#type: ignore
    def apiexception() -> ResponseReturnValue:
        raise ServerException()

    @app.route("/validate")# type: ignore
    def validate() -> ResponseReturnValue:
        AgeSchema.model_validate({"age": "abc"})
        raise ValidationException()

    yield app

@pytest.fixture()
def client(app_with_handlers: Flask) -> FlaskClient:
    return app_with_handlers.test_client()

def test_not_found_handler(client: FlaskClient) -> None:
    resp = client.get("/nonexistent")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["message"] == "The requested resource could not be found"

def test_generic_exception_handler(client: FlaskClient) -> None:
    resp = client.get("/boom")
    assert resp.status_code == 500
    data = resp.get_json()
    assert data["message"] == "Unexpected error"

def test_pydantic_exception_handler(client: FlaskClient) -> None:
    resp = client.get("/validate")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["message"] == "Validation failed"


def test_api_exception_handler(client: FlaskClient) -> None:
    resp = client.get("/apiexception")
    assert resp.status_code == 500
    data = resp.get_json()
    assert data["message"] == "Server error"
