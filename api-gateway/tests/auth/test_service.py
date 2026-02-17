from typing import Generator
from unittest.mock import MagicMock, patch

import httpx
from flask import Flask
import pytest
from flask_jwt_extended import decode_token

from webapp import create_app
from webapp.services.auth.dtos import LoginDTO, LoginMfaRequiredDTO, TokenPairDTO, VerifyMfaDTO
from webapp.services.auth.services import AuthService
from webapp.services.exceptions import ValidationException


@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
        "USERS_SERVICE_URL": "http://localhost:users-webapp",
        "HTTP_TIMEOUT": 5,
    })
    return app

@pytest.fixture
def service(app: Flask) -> Generator[AuthService, None, None]:
    with app.app_context():
        yield AuthService()

def make_response(json_data: dict, status_code: int = 200) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.json.return_value = json_data
    resp.status_code = status_code
    return resp


@patch("webapp.services.auth.services.httpx.post")
@patch("webapp.services.auth.services.raise_for_status")
def test_login(mock_raise: MagicMock, mock_post: MagicMock, service: AuthService, app: Flask) -> None:
    dto = LoginDTO(identifier="test", password="123456")
    mock_post.return_value = make_response({
        "id": "1",
        "is_active": True,
        "mfa_secret": "",
    }, 201)


    with app.app_context():
        result = service.login(dto)
    assert isinstance(result, TokenPairDTO)

    payload = decode_token(result.access_token)
    assert payload["sub"] == "1"
    mock_raise.assert_called_once()
    mock_post.assert_called_once_with("http://localhost:users-webapp/auth/check", json=dto.__dict__, timeout=5)

@patch("webapp.services.auth.services.httpx.post")
@patch("webapp.services.auth.services.raise_for_status")
def test_login_if_user_not_active(mock_raise: MagicMock, mock_post: MagicMock, app: Flask, service: AuthService) -> None:
    dto = LoginDTO(identifier="test", password="123456")
    mock_post.return_value = make_response({
        "id": "1",
        "is_active": False,
        "mfa_secret": ""
    })
    with pytest.raises(ValidationException, match="User is not active"):
        service.login(dto)
    mock_raise.assert_called_once()
    mock_post.assert_called_once_with(
        "http://localhost:users-webapp/auth/check", json=dto.__dict__, timeout=5
    )

@patch("webapp.services.auth.services.httpx.post")
@patch("webapp.services.auth.services.raise_for_status")
def test_login_if_user_mfa_secret(mock_raise: MagicMock, mock_post: MagicMock, app: Flask, service: AuthService) -> None:
    dto = LoginDTO(identifier="test", password="123456")
    mock_post.return_value = make_response({
        "id": "1",
        "is_active": True,
        "mfa_secret": "secret123"
    })
    with app.app_context():
        result = service.login(dto)

    assert isinstance(result, LoginMfaRequiredDTO)
    assert result.mfa_required is True
    mock_raise.assert_called_once()
    mock_post.assert_called_once_with("http://localhost:users-webapp/auth/check", json=dto.__dict__, timeout=5)


@patch("webapp.services.auth.services.httpx.get")
@patch("webapp.services.auth.services.raise_for_status")
@patch("webapp.services.auth.services.pyotp.TOTP.verify")
def test_verify_mfa(mock_verify: MagicMock, mock_raise: MagicMock, mock_get: MagicMock, service: AuthService, app: Flask) -> None:
    dto = VerifyMfaDTO(user_id="123", code="code123")
    mock_get.return_value = make_response({
        "id": "1",
        "is_active": True,
        "mfa_secret": "secret123"
    })

    mock_verify.return_value = True
    with app.app_context():
        result = service.verify_mfa(dto)

    assert isinstance(result, TokenPairDTO)
    payload = decode_token(result.access_token)
    assert payload["sub"] == "1"
    mock_raise.assert_called_once()
    mock_verify.assert_called_once_with('code123', valid_window=1)

@patch("webapp.services.auth.services.httpx.get")
@patch("webapp.services.auth.services.raise_for_status")
@patch("webapp.services.auth.services.pyotp.TOTP.verify")
def test_verify_mfa_if_not_secret(
        mock_verify: MagicMock,
        mock_raise: MagicMock,
        mock_get: MagicMock,
        service: AuthService,
        app: Flask
) -> None:
    dto = VerifyMfaDTO(user_id="123", code="code123")
    mock_get.return_value = make_response({
        "id": "1",
        "is_active": True,
        "mfa_secret": ""
    })

    mock_verify.return_value = False
    with pytest.raises(ValidationException, match="Mfa is not enabled for this user"):
        service.verify_mfa(dto)
    mock_raise.assert_called_once()
    mock_verify.assert_not_called()
    mock_get.assert_called_once_with("http://localhost:users-webapp/id", params=dto.__dict__, timeout=5)

@patch("webapp.services.auth.services.httpx.get")
@patch("webapp.services.auth.services.raise_for_status")
@patch("webapp.services.auth.services.pyotp.TOTP.verify")
def test_verify_mfa_if_not_totp_verify(
        mock_verify: MagicMock,
        mock_raise: MagicMock,
        mock_get: MagicMock,
        service: AuthService,
        app: Flask
) -> None:
    dto = VerifyMfaDTO(user_id="123", code="code123")
    mock_get.return_value = make_response({
        "id": "1",
        "is_active": True,
        "mfa_secret": "secret123"
    })
    mock_verify.return_value = False

    with pytest.raises(ValidationException, match="Mfa verification failed"):
        service.verify_mfa(dto)


    mock_raise.assert_called_once()
    mock_verify.assert_called_once()
    mock_get.assert_called_once_with("http://localhost:users-webapp/id", params=dto.__dict__, timeout=5)





