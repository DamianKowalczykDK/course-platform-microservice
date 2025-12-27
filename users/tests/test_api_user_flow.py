
from urllib.parse import urlparse
from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient
from flask import Flask
from testcontainers.mongodb import MongoDbContainer
from typing import Generator

from webapp import create_app
from webapp.database.models.user import User
from webapp.settings import Config
import pytest
import urllib

@pytest.fixture(scope="module")
def mongo_db_container_url() -> Generator[str, None, None]:
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo.get_connection_url()

@pytest.fixture
def app(mongo_db_container_url: str) -> Generator[Flask, None, None]:
    parsed = urlparse(mongo_db_container_url)

    Config.MONGODB_DB = parsed.path.lstrip("/")
    Config.MONGODB_HOST = parsed.hostname or "localhost"
    Config.MONGODB_PORT = parsed.port or 27017
    if parsed.username:
        Config.MONGODB_USERNAME = parsed.username

    if parsed.password:
        Config.MONGODB_PASSWORD = parsed.password

    app: Flask = create_app()
    app.config.update(
        TESTING=True,
        USER_ACTIVATION_EXPIRATION_MINUTES=5,
        RESET_PASSWORD_EXPIRATION_MINUTES=5
    )

    yield app
    User.drop_collection()

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@patch("webapp.services.email_service.EmailService.send_email")
def test_user_flow(mock_email: MagicMock, client: FlaskClient) -> None:
        resp = client.post("/api/users/",
            json={
                "username": "Jon30",
                "first_name": "Jon",
                "last_name": "Doe",
                "email": "jon@example.com",
                "password": "secret123",
                "password_confirmation": "secret123",
                "gender": "Male",
                "role": "user",
            }
            )

        assert resp.status_code == 201
        data = resp.get_json()
        assert data["is_active"] is False

        user = User.objects.get(username="Jon30")
        user_identifier = user.username

        resp = client.get("/api/users/activation/resend", query_string={"identifier": user_identifier})
        assert resp.status_code == 200

        user = User.objects.get(username="Jon30")
        activation_code = user.activation_code

        resp = client.patch("/api/users/activation", json={"code": activation_code})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["is_active"] is True

        resp = client.get("/api/users/identifier", query_string={"identifier": user_identifier})
        assert resp.status_code == 200

        data = resp.get_json()
        user_id= data["id"]

        resp = client.get(f"/api/users/id", query_string={"user_id": user_id})
        assert resp.status_code == 200

        resp = client.post("/api/users/auth/check", json={"identifier": "Jon30", "password": "secret123"})
        assert resp.status_code == 200


        resp = client.post("/api/users/password/forgot", json={"identifier": "Jon30"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["message"] == "If the email exist, a reset link has been sent."

        user.reload()
        reset_token = user.reset_password_token
        assert reset_token is not None

        resp = client.post("/api/users/password/reset",
               json={
                   "token": reset_token,
                   "new_password": "newpassword123"
               }
               )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["message"] == "Password has been reset successfully."

        resp = client.patch("/api/users/mfa/enable", json={"user_id": str(user.id)})
        assert resp.status_code == 200
        data = resp.get_json()
        decoded_uri = urllib.parse.unquote(data["provisioning_uri"])
        assert "jon@example.com" in decoded_uri

        resp = client.get("/api/users/mfa/qr", query_string={"user_id": str(user.id)})
        assert resp.status_code == 200

        resp = client.patch("/api/users/mfa/disable", json={"user_id": str(user.id)})
        assert resp.status_code == 200





