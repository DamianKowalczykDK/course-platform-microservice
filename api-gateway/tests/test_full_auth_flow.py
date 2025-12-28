from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch, MagicMock

from flask_jwt_extended import create_access_token, create_refresh_token

from webapp import create_app
from webapp.api.auth.mappers import to_schema_token_pair
from webapp.api.auth.schemas import TokenPairSchema
from webapp.api.users.routes import activate_user
from webapp.api.users.schemas import GenderType
from webapp.services.auth.dtos import LoginMfaRequiredDTO, TokenPairDTO, VerifyMfaDTO
from webapp.services.users.dtos import UserDTO, MfaSetupDTO, GetMfaDTO
import pytest

@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@patch("webapp.services.users.services.UserService.get_mfa_qr_code")
@patch("webapp.services.auth.services.AuthService.verify_mfa")
@patch("webapp.services.auth.services.AuthService.login")
@patch("webapp.services.users.services.UserService.disable_mfa")
@patch("webapp.services.users.services.UserService.enable_mfa")
@patch("webapp.services.users.services.UserService.reset_password")
@patch("webapp.services.users.services.UserService.forgot_password")
@patch("webapp.services.users.services.UserService.get_user_by_identifier")
@patch("webapp.services.users.services.UserService.get_user_by_id")
@patch("webapp.services.users.services.UserService.resend_activation_code")
@patch("webapp.services.users.services.UserService.activate_user")
@patch("webapp.services.users.services.UserService.create_user")
def test_full_auth_flow(
        mock_create_user: MagicMock,
        mock_activate_user: MagicMock,
        mock_resend_activation_code: MagicMock,
        mock_get_user_by_id: MagicMock,
        mock_get_by_identifier: MagicMock,
        mock_forgot_password: MagicMock,
        mock_reset_password: MagicMock,
        mock_enable_mfa: MagicMock,
        mock_disable_mfa: MagicMock,
        mock_login: MagicMock,
        mock_verify_mfa: MagicMock,
        mock_get_mfa_qr_code: MagicMock,
        client: FlaskClient,
        app: Flask

) -> None:

    fake_user = UserDTO(
        id="id1234",
        username="TestUser",
        first_name="TestFirstName",
        last_name="TestLastName",
        email="test@example.com",
        gender=GenderType.MALE,
        role="admin",
        is_active=False,
        mfa_secret=""
    )

    mock_create_user.return_value = fake_user

    resp = client.post("/api/users", json={
        "username": "TestUser",
        "first_name": "TestFirstName",
        "last_name": "TestLastName",
        "email": "test@example.com",
        "password": "secret123",
        "password_confirmation": "secret123",
        "gender": "Male",
        "role": "admin",

    })

    assert resp.status_code == 201
    mock_create_user.assert_called_once()

    activate_user = fake_user.__class__(**{**fake_user.__dict__, "is_active": True})
    mock_activate_user.return_value =activate_user
    resp = client.patch("/api/users/activation", json={"code": "code123"})

    assert resp.status_code == 200
    assert resp.get_json()["is_active"] is True
    mock_activate_user.assert_called_once()

    mock_resend_activation_code.return_value = activate_user
    resp = client.get("/api/users/activation/resend", query_string={"identifier": "test@example.com"})
    assert resp.status_code == 200
    mock_resend_activation_code.assert_called_once()

    mock_get_user_by_id.return_value = activate_user
    resp = client.get("/api/users/id", query_string={"user_id": fake_user.id})
    assert resp.status_code == 200
    with app.app_context():
        valid_token = create_access_token(identity="TestUser")
        resp = client.get("/api/protected/admin-only", headers={"Authorization": f"Bearer {valid_token}"})
        assert resp.status_code == 200
        assert mock_resend_activation_code.call_count == 1

        resp = client.get("/api/protected/any-authenticated", headers={"Authorization": f"Bearer {valid_token}"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["Message"] == "Hello, authenticated user!"

        resp = client.get("/api/protected/user-only", headers={"Authorization": f"Bearer {valid_token}"})
        assert resp.status_code == 403
        data = resp.get_json()
        assert data["Message"] == "Forbidden"


    mock_get_by_identifier.return_value = fake_user
    resp = client.get("/api/users/identifier", query_string={"identifier": fake_user.username})
    assert resp.status_code == 200
    mock_get_by_identifier.assert_called_once()

    mock_forgot_password.return_value = fake_user
    resp = client.post("/api/users/password/forgot", json={"identifier": fake_user.username})
    assert resp.status_code == 200
    mock_forgot_password.assert_called_once()

    mock_reset_password.return_value = fake_user
    resp = client.post("/api/users/password/reset", json={"token": "token1234", "new_password": "new123"})
    assert resp.status_code == 200
    mock_reset_password.assert_called_once()

    mfa_setup = MfaSetupDTO(
        user_id=fake_user.id,
        provisioning_uri="otpauth://totp/Example:testuser?secret=SECRET",
        qr_code_base64="3457987dsbfbsb32476"
    )

    mock_enable_mfa.return_value = mfa_setup
    resp = client.patch("/api/users/mfa/enable", json={"user_id": fake_user.id})
    assert resp.status_code == 200
    mock_enable_mfa.assert_called_once()

    mock_get_mfa_qr_code.return_value = mfa_setup
    resp = client.get("/api/users/mfa/qr", query_string={"user_id": fake_user.id})
    assert resp.status_code == 200


    mock_disable_mfa.return_value = fake_user
    resp = client.patch("/api/users/mfa/disable", json={"user_id": fake_user.id})
    assert resp.status_code == 200
    mock_disable_mfa.assert_called_once()

    mock_login.return_value = LoginMfaRequiredDTO(mfa_required=True, user_id=fake_user.id)
    resp = client.post("/api/auth/login", json={"identifier": fake_user.username, "password": "pass1234"})
    assert resp.status_code == 200


    tokens_pair_dto = TokenPairDTO(access_token="access_token", refresh_token="refresh_token")
    mock_login.return_value = tokens_pair_dto
    resp = client.post("/api/auth/login", json={"identifier": fake_user.username, "password": "pass1234"})
    assert resp.status_code == 200
    assert mock_login.call_count == 2





    mock_verify_mfa.return_value = tokens_pair_dto
    resp = client.post("/api/auth/mfa/verify", json={"user_id": "id789", "code": "code123"})
    assert resp.status_code == 200
    mock_verify_mfa.assert_called_once()

    resp = client.post("/api/auth/logout")
    assert resp.status_code == 200

@patch("webapp.services.users.services.UserService.get_user_by_id")
def test_user_role(mock_get_user_by_id: MagicMock, app: Flask, client: FlaskClient) -> None:
    user = UserDTO(
        id="id12345",
        username="UserTest",
        first_name="TestFirstName",
        last_name="TestLastName",
        email="testuser@example.com",
        gender=GenderType.MALE,
        role="user",
        is_active=True,
        mfa_secret=""
    )

    mock_get_user_by_id.return_value = user
    valid_token = create_access_token(identity="TestUser")
    resp = client.get("/api/protected/user-only", headers={"Authorization": f"Bearer {valid_token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["Message"] == "Hello, User!"


@patch("webapp.services.auth.services.AuthService.generate_token")
def test_refresh_token(mock_generate_token: MagicMock,  app: Flask, client: FlaskClient) -> None:
    token_pair = TokenPairDTO(access_token="access_token", refresh_token="refresh_token")
    schema = to_schema_token_pair(token_pair)

    mock_generate_token.return_value = schema

    with app.app_context():
        refresh_token = create_refresh_token(identity="id12345")

    client.set_cookie(key="refresh_token_cookie", value=refresh_token)

    resp = client.post("/api/auth/refresh")
    data = resp.get_json()
    assert "access_token" in data
    assert resp.status_code == 200

    mock_generate_token.assert_called_once()




























