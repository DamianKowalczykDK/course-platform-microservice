from webapp.services.exceptions import ValidationException, ServerException
from webapp import register_error_handlers
from pydantic import BaseModel
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
from flask.typing import ResponseReturnValue
import pytest


class AgeTestSchema(BaseModel):
    age: int

@pytest.fixture
def app_with_handler() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    register_error_handlers(app)

    @app.route('/boom')
    def boom() -> ResponseReturnValue:
        raise RuntimeError("BOOM!")

    @app.route('/apiexception')
    def apiexception() -> ResponseReturnValue:
        raise ServerException()

    @app.route('/validation')
    def validation() -> ResponseReturnValue:
        AgeTestSchema.model_validate({"age": "bad"})
        raise ValidationException()

    @app.route('/validate')
    def validate() -> ResponseReturnValue:
        # AgeTestSchema.model_validate({"age": "bad"})
        # raise ValidationException()
        try:
            AgeTestSchema.model_validate({"age": "bad"})
        except Exception:
            raise ValidationException("Validation failed")
    yield app

@pytest.fixture
def client(app_with_handler: Flask) -> FlaskClient:
    return app_with_handler.test_client()

def test_not_found(client: FlaskClient) -> None:
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'The requested resource was not found.'

def test_server_error(client: FlaskClient) -> None:
    response = client.get('/boom')
    assert response.status_code == 500
    data = response.get_json()
    assert data['message'] == 'Unexpected server error.'

def test_validation_error(client: FlaskClient) -> None:
    response = client.get('/validate')
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Validation failed'

def test_api_exception(client: FlaskClient) -> None:
    response = client.get('/apiexception')
    assert response.status_code == 500
    data = response.get_json()
    assert data['message'] == 'Server error'

def test_validation_exception(client: FlaskClient) -> None:
    response = client.get('/validation')
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Validation failed'



