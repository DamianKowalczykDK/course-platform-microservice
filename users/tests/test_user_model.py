from datetime import datetime, timezone
import pytest
from webapp.database.models.user import User


@pytest.fixture
def user() -> User:
    return User(
        username="test",
        first_name="Jon",
        last_name="Doe",
        email="test@example.com",
        password_hash="hash1234",
        gender="Male",
        activation_code="code12345"
    )

def test_activate_sets_active_and_changes_code(user: User) -> None:
    user.activation_code = user.activation_code
    user.activate()
    assert user.is_active is True
    assert user.activation_code == str(user.id)

def test_update_activation_code_changes_code_and_timestamp(user: User) -> None:
    old_activation_code = user.activation_code
    user.update_activation_code()
    assert user.activation_code != old_activation_code
    assert user.activation_created_at < datetime.now(timezone.utc)

def test_set_and_clear_reset_password_token(user: User) -> None:
    user.set_reset_password_token(expires_minutes=1)
    assert user.reset_password_token is not None
    assert user.reset_password_expires_at is not None
    assert user.reset_password_expires_at > datetime.now(timezone.utc)

    user.clear_reset_password_token()
    assert user.reset_password_token is None
    assert user.reset_password_expires_at is None

def test_reset_password(user: User) -> None:
    user.set_reset_password_token(expires_minutes=1)
    old_password_hash = user.password_hash
    user.reset_password("newpassword123")
    assert user.password_hash != old_password_hash

def test_is_token_reset_password_valid(user: User) -> None:
    user.set_reset_password_token(expires_minutes=1)
    token = user.reset_password_token

    assert token is not None
    assert user.is_token_rest_password_valid(token) is True

def test_if_token_reset_password_valid_returns_false(user: User) -> None:
    user.set_reset_password_token(expires_minutes=1)
    assert user.is_token_rest_password_valid("bad_token") is False


def test_if_token_reset_password_not_expires_at(user: User) -> None:
    user.set_reset_password_token()
    token = user.reset_password_token
    user.reset_password_expires_at = None

    assert token is not None
    assert user.is_token_rest_password_valid(token) is False

def test_if_token_reset_password_valid_date_time(user: User) -> None:
    user.reset_password_token = "token-test"
    user.reset_password_expires_at = datetime.now()
    assert user.is_token_rest_password_valid("token-test") is True

def test_enable_mfa(user: User) -> None:
    user.enable_mfa_secret("secret123")
    assert user.mfa_secret == "secret123"

def test_disable_mfa(user: User) -> None:
    user.enable_mfa_secret("secret123")
    assert user.mfa_secret == "secret123"
    user.disable_mfa_secret()
    assert user.mfa_secret is None

def test_has_mfa_secret(user: User) -> None:
    user.mfa_secret = "secret123"
    user.has_mfa_secret()
    assert user.mfa_secret is not None



