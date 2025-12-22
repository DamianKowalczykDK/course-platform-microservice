from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock
from flask import Flask
from werkzeug.security import check_password_hash
from urllib.parse import unquote
from webapp.database.models.user import GenderType, User
from webapp.services.exceptions import NotFoundException, ValidationException, ConflictException
from webapp.services.users.dtos import (
    CreateUserDTO,
    EnableMfaDTO, DisableMfaDTO,
    GetMfaQrCodeDTO,
    ResetPasswordDTO,
    LoginUserDTO,
    ForgotPasswordDTO
)
from webapp.services.users.services import UserService
import pyotp
import pytest
import urllib


@pytest.fixture
def mock_user_repository() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_email_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def flask_app() -> Flask:
    app = Flask(__name__)
    app.config['RESET_PASSWORD_EXPIRATION_MINUTES'] = 15
    return app

@pytest.fixture
def user_service(mock_user_repository: MagicMock, mock_email_service: MagicMock) -> UserService:
    return UserService(
        user_repository=mock_user_repository,
        email_service=mock_email_service
    )

def test_creat_user_and_send_activation_email(
        user_service: UserService,
        mock_user_repository: MagicMock,
        mock_email_service: MagicMock
) -> None:

    dto = CreateUserDTO(
        username="test_user",
        password="hash1234",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test_email@example.com",
        gender=GenderType.MALE,

    )
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.get_by_username.return_value = None

    result = user_service.create_user(dto)

    mock_user_repository.create_user.assert_called_once()
    saved_user = mock_user_repository.create_user.call_args[0][0]
    assert saved_user.username == "test_user"
    assert saved_user.first_name == "test_first_name"
    assert saved_user.last_name == "test_last_name"
    assert check_password_hash(saved_user.password_hash, "hash1234")

    mock_email_service.send_email.assert_called_once()

    assert  result.is_active is False

def test_create_user_if_email_exists(user_service: UserService, mock_user_repository: MagicMock) -> None:
    dto = CreateUserDTO(
        username="test_user",
        password="hash1234",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test_email@example.com",
        gender=GenderType.MALE,

    )
    mock_user_repository.get_by_email.return_value = dto.email
    with pytest.raises(ConflictException, match="Email already exists"):
        user_service.create_user(dto)

def test_create_user_if_username_exists(user_service: UserService, mock_user_repository: MagicMock) -> None:
    dto = CreateUserDTO(
        username="test_user1",
        password="hash1234",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test_email1@example.com",
        gender=GenderType.MALE,

    )
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.get_by_username.return_value = dto.username
    with pytest.raises(ConflictException, match="Username already exists"):
        user_service.create_user(dto)

def test_enable_mfa_enable(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = User(
        id="4234dsfsgd98234234",
        username="test_user",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code123"
    )

    mock_user_repository.get_by_id.return_value = user

    dto = EnableMfaDTO(user_id=str(user.id))
    result = user_service.enable_mfa(dto)

    assert result.user_id == str(user.id)

    decoded_uri = urllib.parse.unquote(result.provisioning_uri)
    assert "test@example.com" in decoded_uri

def test_enable_mfa_not_found_raises(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_by_id.return_value = None
    with pytest.raises(NotFoundException, match="User not found"):
        dto = EnableMfaDTO(user_id=str("bad"))
        user_service.enable_mfa(dto)


def test_disable_mfa_success(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = User(
        id="4234dsfsgd98234234",
        username="test_user",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code123",
        mfa_secret="secret"
    )
    mock_user_repository.get_by_id.return_value = user
    dto = DisableMfaDTO(user_id=str(user.id))

    result = user_service.disable_mfa(dto)
    assert result.mfa_secret is None

def test_disable_mfa_if_not_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_by_id.return_value = None
    dto = DisableMfaDTO(user_id="bad")
    with pytest.raises(NotFoundException, match="User not found"):
        user_service.disable_mfa(dto)

def test_disable_mfa_if_user_not_enabled(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = User(
        id="4234dsfsgd98234234",
        username="test_user",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code123",
        mfa_secret=None
    )
    mock_user_repository.get_by_id.return_value = user
    dto = DisableMfaDTO(user_id=str(user.id))
    with pytest.raises(ValidationException, match="MFA is not enabled for this user"):
        user_service.disable_mfa(dto)

def test_get_mfa_qrcode_success(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = User(
        id="4234dsfsgd98234234",
        username="test_user",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code123",
        mfa_secret=pyotp.random_base32()
    )
    mock_user_repository.get_by_id.return_value = user
    dto = GetMfaQrCodeDTO(user_id=str(user.id))
    result = user_service.get_mfa_qrcode(dto)
    assert result.user_id == str(user.id)



def test_get_mfa_qrcode_not_found_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_by_id.return_value = None
    dto = GetMfaQrCodeDTO(user_id="Bad")
    with pytest.raises(NotFoundException, match="User not found"):
        user_service.get_mfa_qrcode(dto)

def test_get_mfa_qrcode_not_enabled(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = User(
        id="4234dsfsgd98234234",
        username="test_user",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code123",
        mfa_secret=None
    )
    mock_user_repository.get_by_id.return_value = user
    dto = GetMfaQrCodeDTO(user_id=str(user.id))
    with pytest.raises(ValidationException, match="MFA is not enabled for this user"):
        user_service.get_mfa_qrcode(dto)

def test_forgot_password_if_not_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_active_by_username_or_email.return_value = None
    dto = ForgotPasswordDTO(identifier="Bad")
    user_service.forgot_password(dto)
    mock_user_repository.save.assert_not_called()


def test_reset_password_if_not_user_or_token_invalid(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_by_reset_password_token.return_value = None
    dto = ResetPasswordDTO(token="Bad", new_password="new_password")
    with pytest.raises(NotFoundException, match="Invalid or expired token"):
        user_service.reset_password(dto)

def test_activate_if_not_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_by_activation_code.return_value = None
    with pytest.raises(NotFoundException, match="Invalid activation code"):
        user_service.activate_user(activation_code="code123")

def test_active_user_if_code_expired(flask_app: Flask, user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = MagicMock()
    user.activation_created_at = datetime.now(timezone.utc) - timedelta(minutes=30)
    mock_user_repository.get_by_activation_code.return_value = user

    with flask_app.app_context():
        flask_app.config["USER_ACTIVATION_EXPIRATION_MINUTES"] = 15
        with pytest.raises(ValueError, match="Activation code expired"):
            user_service.activate_user(activation_code="expired-code")

def test_resend_activation_code_if_not_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_by_username_or_email.return_value = None
    with pytest.raises(NotFoundException, match="Invalid username or email"):
        user_service.resend_activation_code("code123")

def test_resend_activation_code_if_user_active(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = MagicMock()
    mock_user_repository.get_by_activation_code.return_value = user
    user.is_active = True
    with pytest.raises(ValidationException, match="User already activated"):
        user_service.resend_activation_code("code123")

def test_get_by_username_or_email_if_not_active_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_active_by_username_or_email.return_value = None
    with pytest.raises(NotFoundException, match="Active user not found"):
        user_service.get_by_username_or_email("Test30")

def test_get_by_id_success(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = User(
        id="4234dsfsgd98234234",
        username="test_user",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code123",
        mfa_secret=None
    )
    mock_user_repository.get_by_id.return_value = user
    result = user_service.get_by_id(user_id=str(user.id))
    assert result.id == user.id

def test_get_by_id_not_found_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_by_id.return_value = None
    with pytest.raises(NotFoundException, match="Active user not found"):
        user_service.get_by_id("Bad")

def test_verify_credentials_if_not_user(user_service: UserService, mock_user_repository: MagicMock) -> None:
    mock_user_repository.get_active_by_username_or_email.return_value = None
    dto = LoginUserDTO("Test30", "pass1234")
    with pytest.raises(NotFoundException, match="Invalid credentials -1"):
        user_service.verify_credentials(dto)

def test_verify_credentials_invalid_password(user_service: UserService, mock_user_repository: MagicMock) -> None:
    user = User(
        id="4234dsfsgd98234234",
        username="test_user",
        first_name="test_first_name",
        last_name="test_last_name",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code123",
        mfa_secret=None
    )
    mock_user_repository.get_active_by_username_or_email.return_value = user

    check_password_hash(user.password_hash, "hash123")
    dto = LoginUserDTO("Test30", "hash123")
    with pytest.raises(ValidationException, match="Invalid credentials -2"):
        user_service.verify_credentials(dto)





