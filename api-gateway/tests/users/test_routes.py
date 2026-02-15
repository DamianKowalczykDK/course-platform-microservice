from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient
from webapp.services.users.dtos import DeleteUserByIdDTO, DeleteUserByIdentifierDTO


@patch("webapp.services.users.services.UserService.delete_user_by_id")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_delete_user_by_id(
        mock_admin: MagicMock,
        mock_del: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str]
) -> None:
    mock_admin.return_value = MagicMock(id="1", role="admin")
    user = DeleteUserByIdDTO("user123")
    mock_del.return_value = user

    response = client.delete(f"/api/users/id", query_string={"user_id": "user123"}, headers=admin_headers)
    assert response.status_code == 204

    called_dto = mock_del.call_args[0][0]
    assert isinstance(called_dto, DeleteUserByIdDTO)
    assert called_dto.user_id == "user123"

@patch("webapp.services.users.services.UserService.delete_user_by_identifier")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_delete_user_by_identifier(
        mock_admin: MagicMock,
        mock_del: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str]
) -> None:
    mock_admin.return_value = MagicMock(id="1", role="admin")
    user = DeleteUserByIdentifierDTO("user123")
    mock_del.return_value = user

    response = client.delete(f"/api/users/identifier", query_string={"identifier": "user123"}, headers=admin_headers)
    assert response.status_code == 204

    called_dto = mock_del.call_args[0][0]
    assert isinstance(called_dto, DeleteUserByIdentifierDTO)
    assert called_dto.identifier == "user123"

    mock_admin.assert_called_once()
    mock_del.assert_called_once()

