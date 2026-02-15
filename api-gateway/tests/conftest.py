import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from webapp import create_app


@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app
@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def user_headers(app: Flask) -> dict[str, str]:
    with app.app_context():
        token = create_access_token(identity="user123")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(app: Flask) -> dict[str, str]:
    with app.app_context():
        token = create_access_token(identity="admin")
    return {"Authorization": f"Bearer {token}"}