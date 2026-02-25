from unittest.mock import MagicMock, patch

import httpx
from flask import Flask
from typing import Generator
import pytest

from webapp.services.users.dtos import CreateUserDTO, UserDTO, ActivationUserDTO, ResendActivationCodeDTO, \
    ForgotPasswordDTO, ResetPasswordDTO, EnableMfaDTO, UserIdDTO, MfaSetupDTO, IdentifierDTO, DisableMfaDTO, GetMfaDTO, \
    DeleteUserByIdDTO, DeleteUserByIdentifierDTO
from webapp.services.users.services import UserService


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        "USERS_SERVICE_URL": "http://localhost:users-service",
        'HTTP_TIMEOUT': 5
    })
    return app

@pytest.fixture
def service(app: Flask) -> Generator[UserService, None, None]:
    with app.app_context():
        yield UserService()

def make_response(json_data: dict, status: int = 200) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.json.return_value = json_data
    resp.status_code = status
    return resp

@patch("webapp.services.users.services.httpx.post")
@patch("webapp.services.users.services.raise_for_status")
def test_create_user(mock_raise: MagicMock, mock_post: MagicMock, service: UserService, app: Flask) -> None:
    dto = CreateUserDTO(
        username="test",
        first_name="Test",
        last_name="Test",
        email="test@example.com",
        password="123456",
        password_confirmation="123456",
        gender="male",
        role="admin"
    )

    mock_post.return_value = make_response(
        {
        "id": 1,
        "username": "test",
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@example.com",
        "gender": "male",
        "role": "admin",
        "is_active": False,
    }, 201
    )
    with app.test_request_context():
        result = service.create_user(dto)

    assert isinstance(result, UserDTO)
    assert result.username == "test"
    mock_raise.assert_called_once()
    mock_post.assert_called_once()

@patch("webapp.services.users.services.httpx.patch")
@patch("webapp.services.users.services.raise_for_status")
def test_activate_user(mock_raise: MagicMock, mock_patch: MagicMock, service: UserService, app: Flask) -> None:
    dto = ActivationUserDTO("code123")
    mock_patch.return_value = make_response(
        {
            "id": 1,
            "username": "test",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@example.com",
            "gender": "male",
            "role": "admin",
            "is_active": True
        }
    )
    with app.test_request_context():
        result = service.activate_user(dto)

    assert isinstance(result, UserDTO)
    assert result.username == "test"
    assert result.is_active is True
    mock_raise.assert_called_once()
    mock_patch.assert_called_once()

@patch("webapp.services.users.services.httpx.get")
@patch("webapp.services.users.services.raise_for_status")
def test_resend_activation_code(mock_raise: MagicMock, mock_get: MagicMock, service: UserService, app: Flask) -> None:
    dto = ResendActivationCodeDTO(identifier="test@example.com")
    mock_get.return_value = make_response(
        {
            "id": 1,
            "username": "test",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@example.com",
            "gender": "male",
            "role": "admin",
            "is_active": False
        }
    )
    with app.test_request_context():
        result = service.resend_activation_code(dto)

    assert result.email == "test@example.com"
    mock_raise.assert_called_once_with(mock_get.return_value, not_found_message="User test@example.com not found")
    mock_get.assert_called_once()

@patch("webapp.services.users.services.httpx.post")
@patch("webapp.services.users.services.raise_for_status")
def test_forgot_password(mock_raise: MagicMock, mock_post: MagicMock, service: UserService, app: Flask) -> None:
    dto = ForgotPasswordDTO(identifier="test@example.com")
    mock_post.return_value = make_response(
        {
            "id": 1,
            "username": "test",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@example.com",
            "gender": "male",
            "role": "admin",
            "is_active": False
        }
    )
    with app.test_request_context():
        service.forgot_password(dto)

    mock_raise.assert_called_once()
    mock_post.assert_called_once_with("http://localhost:users-service/password/forgot", json=dto.__dict__, timeout=5)

@patch("webapp.services.users.services.httpx.post")
@patch("webapp.services.users.services.raise_for_status")
def test_reset_password(moc_raise: MagicMock, mock_post: MagicMock, service: UserService, app: Flask) -> None:
    dto = ResetPasswordDTO(token="test_token", new_password="1234567")
    mock_post.return_value = make_response(
        {
            "id": 1,
            "username": "test",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@example.com",
            "gender": "male",
            "role": "admin",
            "is_active": False
        }
    )

    with app.test_request_context():
        service.reset_password(dto)
    mock_post.assert_called_once()
    moc_raise.assert_called_once()

@patch("webapp.services.users.services.httpx.patch")
@patch("webapp.services.users.services.raise_for_status")
def test_enable_mfa(mock_raise: MagicMock, mock_patch: MagicMock, service: UserService, app: Flask) -> None:
    dto = EnableMfaDTO(user_id="123")
    mock_patch.return_value = make_response(
        {
            "user_id": "123",
            "provisioning_uri": "uri",
            "qr_code_base64": "qr"
        }
    )
    with app.test_request_context():
        result = service.enable_mfa(dto)

    assert isinstance(result, MfaSetupDTO)
    assert result.provisioning_uri == "uri"
    mock_raise.assert_called_once()
    mock_patch.assert_called_once_with("http://localhost:users-service/mfa/enable", json=dto.__dict__, timeout=5)

@patch("webapp.services.users.services.httpx.get")
@patch("webapp.services.users.services.raise_for_status")
def test_get_user_by_id(mock_raise: MagicMock, mock_get: MagicMock, service: UserService, app: Flask) -> None:
    dto = UserIdDTO(user_id="123")
    mock_get.return_value = make_response(
        {
            "id": 1,
            "username": "test",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@example.com",
            "gender": "male",
            "role": "admin",
            "is_active": False
        }
    )
    with app.test_request_context():
        result = service.get_user_by_id(dto)

    assert result.id == 1
    mock_raise.assert_called_once()
    mock_get.assert_called_once_with("http://localhost:users-service/id", params=dto.__dict__, timeout=5)

@patch("webapp.services.users.services.httpx.get")
@patch("webapp.services.users.services.raise_for_status")
def test_get_user_by_identifier(mock_raise: MagicMock, mock_get: MagicMock, service: UserService, app: Flask) -> None:
    dto = IdentifierDTO(identifier="test@example.com")
    mock_get.return_value = make_response(
        {
            "id": 1,
            "username": "test",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@example.com",
            "gender": "male",
            "role": "admin",
            "is_active": False
        }
    )
    with app.test_request_context():
        result = service.get_user_by_identifier(dto)

    assert result.email == "test@example.com"
    mock_raise.assert_called_once_with(mock_get.return_value, not_found_message="User test@example.com not found")
    mock_get.assert_called_once_with(
        "http://localhost:users-service/identifier",
        params={"identifier": "test@example.com"},
        timeout=5)


@patch("webapp.services.users.services.httpx.patch")
@patch("webapp.services.users.services.raise_for_status")
def test_disable_mfa(mock_raise: MagicMock, mock_patch: MagicMock, service: UserService, app: Flask) -> None:
    dto = DisableMfaDTO(user_id="123")
    mock_patch.return_value = make_response(
        {
            "id": 1,
            "username": "test",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@example.com",
            "gender": "male",
            "role": "admin",
            "is_active": False
        }
    )
    with app.test_request_context():
        result = service.disable_mfa(dto)

    mock_raise.assert_called_once()
    mock_patch.assert_called_once_with("http://localhost:users-service/mfa/disable", json=dto.__dict__, timeout=5)

@patch("webapp.services.users.services.httpx.get")
@patch("webapp.services.users.services.raise_for_status")
def test_get_mfa_qr_code(mock_raise: MagicMock, mock_get: MagicMock, service: UserService, app: Flask) -> None:
    dto = GetMfaDTO(user_id="123")
    mock_get.return_value = make_response(
        {
            "user_id": "123",
            "provisioning_uri": "uri",
            "qr_code_base64": "qr"
        }
    )
    with app.test_request_context():
        result = service.get_mfa_qr_code(dto)

    assert isinstance(result, MfaSetupDTO)
    assert result.provisioning_uri == "uri"
    mock_raise.assert_called_once()
    mock_get.assert_called_once_with("http://localhost:users-service/mfa/qr", params={"user_id": "123"}, timeout=5)

@patch("webapp.services.users.services.httpx.delete")
@patch("webapp.services.users.services.raise_for_status")
def test_delete_user_by_id(mock_raise: MagicMock, mock_delete: MagicMock, service: UserService, app: Flask) -> None:
    dto = DeleteUserByIdDTO(user_id="123")
    mock_delete.return_value = make_response({}, 204)
    with app.test_request_context():
        service.delete_user_by_id(dto)

    mock_raise.assert_called_once()
    mock_delete.assert_called_once_with("http://localhost:users-service/id", params={"user_id": "123"}, timeout=5)

@patch("webapp.services.users.services.httpx.delete")
@patch("webapp.services.users.services.raise_for_status")
def test_delete_user_by_identifier(mock_raise: MagicMock, mock_delete: MagicMock, service: UserService, app: Flask) -> None:
    dto = DeleteUserByIdentifierDTO(identifier="test@example.com")
    mock_delete.return_value = make_response({}, 204)
    with app.test_request_context():
        service.delete_user_by_identifier(dto)

    mock_raise.assert_called_once()
    mock_delete.assert_called_once_with(
        "http://localhost:users-service/identifier",
        params={"identifier": "test@example.com"},
        timeout=5
    )



