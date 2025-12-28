import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
from flask.typing import ResponseReturnValue

from webapp import register_error_handlers


@pytest.fixture()
def app_with_handlers() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    register_error_handlers(app)

    @app.route("/boom")#type: ignore
    def boom() -> ResponseReturnValue:
        raise RuntimeError("BOOM!")

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