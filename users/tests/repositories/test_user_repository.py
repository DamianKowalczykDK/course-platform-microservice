from webapp.database.models.user import User
from webapp.database.repositories.user import UserRepository


def make_user(username: str, email: str, activation_code: str) -> User:
    return User(
        username=username,
        first_name="Jon",
        last_name="Smith",
        email=email,
        gender="Male",
        password_hash="hash123",
        activation_code=activation_code
    )

def test_create_and_get_methods(user_repository: UserRepository) -> None:
    user = make_user("test_user", "test@example.com", "code1234")
    saved_user = user_repository.create_user(user)
    found = user_repository.get_by_id(str(saved_user.id))

    assert found is not None
    assert found.username == "test_user"

    assert user_repository.get_by_id(str(user.id)) is not None
    assert user_repository.get_by_username_or_email("test@example.com") is not None
    assert user_repository.get_by_username("test_user") is not None
    assert user_repository.get_by_email("test@example.com") is not None


def test_get_active_and_get_by_activation_code(user_repository: UserRepository) -> None:
    user = make_user("test_user1", "test1@example.com", "code123")
    user_repository.create_user(user)

    found_user = user_repository.get_by_activation_code(user.activation_code)

    assert found_user is not None
    assert found_user.username == "test_user1"
    user.is_active = True
    user_repository.save(user)

    assert user_repository.get_active_by_username_or_email("test_user1") is not None

def test_get_by_reset_password_token(user_repository: UserRepository) -> None:
    user = make_user("test_user2", "test2@example.com", "test123")
    user.reset_password_token = "token-test"
    user_repository.create_user(user)

    found_user = user_repository.get_by_reset_password_token("token-test")

    assert found_user is not None
    assert found_user.reset_password_token == "token-test"

def test_delete_user_by_id(user_repository: UserRepository) -> None:
    user = make_user("test3", "test3@example.com", "t123")
    user_repository.create_user(user)

    found_user = user_repository.get_by_id(str(user.id))
    assert found_user is not None
    assert found_user.username == "test3"

    user_repository.delete_user_by_id(str(user.id))
    result = user_repository.get_by_id(user.id)

    assert result is None

def test_delete_user_by_id_if_not_user(user_repository: UserRepository) -> None:
    fake_id = "507f1f77bcf86cd799439011"
    result = user_repository.delete_user_by_id(fake_id)
    assert result is False

def test_delete_user_by_identifier(user_repository: UserRepository) -> None:
    user = make_user("test4", "test4@example.com", "t123")
    user_repository.create_user(user)
    found_user = user_repository.get_by_username_or_email("test4@example.com")
    assert found_user is not None
    user_repository.delete_user_by_identifier(user.email)
    result = user_repository.get_by_id(str(user.id))
    assert result is None

def test_delete_user_by_identifier_if_not_user(user_repository: UserRepository) -> None:
    fake_identifier = "t@example.com"
    result = user_repository.delete_user_by_identifier(fake_identifier)
    assert result is False






