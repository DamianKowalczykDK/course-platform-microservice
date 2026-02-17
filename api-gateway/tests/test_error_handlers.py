from webapp.services.exceptions import ApiException, ServerException, NotFoundException
from webapp import register_error_handlers
from flask.typing import ResponseReturnValue
from flask.testing import FlaskClient
from flask import Flask
from typing import Generator
import pytest


@pytest.fixture
def app_with_error_handlers() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    register_error_handlers(app)

    @app.route('/boom')
    def boom() -> ResponseReturnValue:
        raise RuntimeError('boom')

    @app.route("/apiexception")
    def api_exception() -> ResponseReturnValue:
        raise ServerException()

    @app.route("/non-exist")
    def test_non_found() -> ResponseReturnValue:
        raise NotFoundException()

    @app.route("/exception")
    def exception() -> ResponseReturnValue:
        raise ApiException(message="Test",status_code=400, error_code="validation_error", details=["Test"])

    yield app

@pytest.fixture
def client(app_with_error_handlers: Flask) -> FlaskClient:
    return app_with_error_handlers.test_client()

def test_server_error(client: FlaskClient) -> None:
    response = client.get('/boom')
    assert response.status_code == 500
    data = response.get_json()
    assert data['message'] == "Unexpected error."


def test_api_exception(client: FlaskClient) -> None:
    response = client.get('/apiexception')
    assert response.status_code == 500
    data = response.get_json()
    assert data['message'] == "Server error"


def test_not_found(client: FlaskClient) -> None:
    response = client.get("/nonexist")
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "not_found"



def test_not_found_exception(client: FlaskClient) -> None:
    response = client.get("/non-exist")
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == "Resource not found"

def test_register_error_handlers(client: FlaskClient) -> None:
    response = client.get('/exception')
    assert response.status_code == 400
    data = response.get_json()
    assert data["details"]  == ["Test"]



























