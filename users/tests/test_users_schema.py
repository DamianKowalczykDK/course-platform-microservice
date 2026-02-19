import pytest
from webapp.api.users.schemas import CreateUserSchema
from webapp.database.models.user import GenderType

def test_passwords_invalid() -> None:
    with pytest.raises(ValueError, match="Passwords don't match") :
        CreateUserSchema(
            username="user123",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="Secret123.",
            password_confirmation="different123.",
            gender=GenderType.MALE,
            role="user",
        )

def test_passwords_match() -> None:
    user = CreateUserSchema(
        username="user123",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="Secret123.",
        password_confirmation="Secret123.",
        gender=GenderType.MALE,
        role="user"
    )
    assert user.password == user.password_confirmation
        
def test_passwords_regex_invalid() -> None:
    with pytest.raises(ValueError, match="Password must have at least 1 uppercase, 1 lowercase, 1 digit, "
                "1 special char, and be at least 8 characters long") :
        CreateUserSchema(
            username="user123",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="Secret123",
            password_confirmation="different123.",
            gender=GenderType.MALE,
            role="user",
        )


