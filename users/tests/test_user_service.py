from datetime import datetime
from unittest.mock import MagicMock
from werkzeug.security import check_password_hash
import pytest

from webapp.database.models.user import GenderType
from webapp.services.users.dtos import CreateUserDTO, ReadUserDTO
from webapp.services.users.services import UserService


@pytest.fixture
def mock_user_repository() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_email_service() -> MagicMock:
    return MagicMock()

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

    # read_dto = ReadUserDTO(
    #     id=str("sdfgsd"),
    #     username = dto.username,
    #     first_name = dto.first_name,
    #     last_name = dto.last_name,
    #     email = dto.email,
    #     gender = GenderType(dto.gender),
    #     role = "user",
    #     is_active =  False,
    #     created_at = datetime.now()
    # )
    # mock_user_repository.get_active_by_username_or_email.return_value = read_dto
    # activate = user_service.get_by_username_or_email("test_user")
    # assert activate.is_active is False

