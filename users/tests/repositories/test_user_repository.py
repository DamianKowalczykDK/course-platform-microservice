from datetime import datetime, timezone

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
    found = user_repository.get_user_by_id(str(saved_user.id))
    assert found is not None
    assert found.username == "test_user"

    assert user_repository.get_user_by_id(str(user.id)) is not None
    assert user_repository.get_by_username_or_email("test@example.com") is not None
    assert user_repository.get_by_username("test_user") is not None
    assert user_repository.get_by_email("test@example.com") is not None

    all_users = user_repository.get_all()
    assert any(u.username == "test_user" for u in all_users)

def test_get_active_and_get_by_activation_code(user_repository: UserRepository) -> None:
    user = make_user("test_user1", "test1@example.com", "code123")
    user_repository.create_user(user)

    found_user = user_repository.get_by_activation_code(user.activation_code)
    assert found_user is not None
    assert found_user.username == "test_user1"
    assert user_repository.get_active_by_username_or_email("test_user1") is None

def test_update_activation_code_and_activate_user(user_repository: UserRepository) -> None:
    user = make_user("test_user2", "test2@example.com", "code12")
    saved_user = user_repository.create_user(user)

    updated = user_repository.update_activation_code(saved_user)
    assert updated.activation_code != "code12"
    assert updated.updated_at < datetime.now(timezone.utc)

    user_repository.activate(updated)
    activated = user_repository.get_active_by_username_or_email("test_user2")
    assert activated.is_active is True
