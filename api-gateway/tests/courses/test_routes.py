from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient
from webapp.services.courses.dtos import CourseDTO, CourseIdDTO, CourseNameDTO, UpdateCourseDTO
import pytest

@pytest.fixture
def course() -> CourseDTO:
    return CourseDTO(
        id=1,
        name="Test Course",
        description="Test Course",
        price=100,
        start_date="2026-01-10",
        end_date="2026-01-20"
    )

@patch("webapp.services.courses.services.CourseService.create_course")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_create_course(
        mock_admin: MagicMock,
        mock_create: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str],
        course: CourseDTO
) -> None:
    mock_admin.return_value = MagicMock(id="1", role="admin")

    mock_create.return_value = course
    response = client.post(f"/api/course", json=course.__dict__, headers=admin_headers)
    assert response.status_code == 201

    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Test Course"
    mock_admin.assert_called_once()
    mock_create.assert_called_once()

@patch("webapp.services.courses.services.CourseService.get_by_id")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_get_by_id(
        mock_admin: MagicMock,
        mock_get: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str],
        course: CourseDTO
) -> None:
    mock_admin.return_value = MagicMock(id="1", role="admin")
    mock_get.return_value = course

    resp = client.get(f"/api/course/{course.id}", headers=admin_headers)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["id"] == 1

    mock_get.assert_called_once_with(CourseIdDTO(1))
    mock_admin.assert_called_once()

@patch("webapp.services.courses.services.CourseService.get_by_name")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_get_by_name(
        mock_admin: MagicMock,
        mock_get: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str],
        course: CourseDTO
) -> None:
    mock_admin.return_value = MagicMock(id="1", role="admin")
    mock_get.return_value = course

    resp = client.get(f"/api/course/",query_string={"name": "Test Course"}, headers=admin_headers)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["price"] == 100

    mock_get.assert_called_once_with(CourseNameDTO("Test Course"))
    mock_admin.assert_called_once()



@patch("webapp.services.courses.services.CourseService.update_course")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_update_course(
        mock_admin: MagicMock,
        mock_update: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str],
        course: CourseDTO
) -> None:
    mock_admin.return_value = MagicMock(id="1", role="admin")

    course_update = UpdateCourseDTO(
        id=1,
        name="Test1",
        description=None,
        price=None,
        start_date=None,
        end_date=None
    )
    mock_update.return_value = course
    resp = client.patch(f"/api/course/1",json={"name": "Test1"}, headers=admin_headers)
    assert resp.status_code == 200

    update = mock_update.call_args[0][0]
    assert update.name == "Test1"

    mock_update.assert_called_once_with(course_update)
    mock_admin.assert_called_once()

@patch("webapp.services.courses.services.CourseService.delete_by_id")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_delete_by_id(
        mock_admin: MagicMock,
        mock_del: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str],
        course: CourseDTO
) -> None:
    mock_admin.return_value = MagicMock(id="1", role="admin")

    mock_del.return_value = course
    resp = client.delete(f"/api/course/{course.id}", headers=admin_headers)
    assert resp.status_code == 204

    mock_admin.assert_called_once()
    mock_del.assert_called_once_with(CourseIdDTO(1))


