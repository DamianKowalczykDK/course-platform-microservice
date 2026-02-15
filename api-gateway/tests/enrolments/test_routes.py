from unittest.mock import MagicMock, patch
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from webapp import create_app
import pytest
from webapp.services.enrolments.dtos import (
    EnrolmentDTO,
    PaymentStatus,
    Status,
    EnrolmentIdDTO,
    EnrolmentByUserDTO,
    DeleteEnrolmentDTO
)
from webapp.services.users.dtos import UserIdDTO


@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app
@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def user_headers(app: Flask) -> dict[str, str]:
    with app.app_context():
        token = create_access_token(identity="user123")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(app: Flask) -> dict[str, str]:
    with app.app_context():
        token = create_access_token(identity="admin")
    return {"Authorization": f"Bearer {token}"}

@patch("webapp.api.enrolments.routes.EnrolmentService.create_enrolment_for_user")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_create_enrolment_for_user(
        mock_user: MagicMock,
        mock_creat: MagicMock,
        client: FlaskClient,
        user_headers: dict[str, str]
) -> None:
    mock_user.return_value = MagicMock(id="user123", role="user")
    enrolment = EnrolmentDTO(
        id=1,
        user_id="user123",
        course_id=1,
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PENDING,
    )
    mock_creat.return_value = enrolment

    resp = client.post(f"/api/enrolment", json={
        "id": 1,
        "user_id": "user123",
        "course_id": 1,
        "status": Status.ACTIVE.value,
        "payment_status": PaymentStatus.PENDING.value,
    }, headers=user_headers)

    assert resp.status_code == 201
    mock_user.assert_called_once_with(UserIdDTO("user123"))
    mock_creat.assert_called_once()

@patch("webapp.api.enrolments.routes.EnrolmentService.set_paid")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_set_paid(
        mock_user: MagicMock,
        mock_paid: MagicMock,
        client: FlaskClient,
        user_headers: dict[str, str]
) -> None:
    mock_user.return_value = MagicMock(id="user123", role="user")

    enrolment = EnrolmentDTO(
        id=1,
        user_id="user123",
        course_id=1,
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PAID,
    )
    mock_paid.return_value = enrolment
    resp = client.patch(f"/api/enrolment/paid", json={"enrolment_id": 1}, headers=user_headers
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 1

    mock_paid.assert_called_once_with(EnrolmentIdDTO(1))
    mock_user.assert_called_once_with(UserIdDTO("user123"))

@patch("webapp.api.enrolments.routes.EnrolmentService.expired_courses")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_expired_courses(
        mock_admin: MagicMock,
        mock_expired: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str]
) -> None:
    mock_admin.return_value = MagicMock(id="admin123", role="admin")

    enrolment = [EnrolmentDTO(
        id=1,
        user_id="admin123",
        course_id=1,
        status=Status.COMPLETED,
        payment_status=PaymentStatus.PAID)]

    mock_expired.return_value = enrolment
    resp = client.patch(f"/api/enrolment/expired", headers=admin_headers)

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["enrolments"][0]["user_id"] == "admin123"
    mock_admin.assert_called_once()
    mock_expired.assert_called_once()

@patch("webapp.api.enrolments.routes.EnrolmentService.get_by_id")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_get_by_id(
        mock_admin: MagicMock,
        mock_get: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str]
) -> None:
    mock_admin.return_value = MagicMock(id="admin123", role="admin")
    enrolment = EnrolmentDTO(
        id=1,
        user_id="user123",
        course_id=1,
        status=Status.COMPLETED,
        payment_status=PaymentStatus.PAID,
    )
    mock_get.return_value = enrolment
    resp = client.get(f"/api/enrolment/{enrolment.id}", headers=admin_headers)
    assert resp.status_code == 200

    mock_get.assert_called_once_with(EnrolmentIdDTO(1))
    mock_admin.assert_called_once()

@patch("webapp.api.enrolments.routes.EnrolmentService.get_by_id_and_user")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_get_by_id_and_user(
        mock_user: MagicMock,
        mock_get: MagicMock,
        client: FlaskClient,
        user_headers: dict[str, str]
) -> None:
    mock_user.return_value = MagicMock(id="user123", role="user")
    enrolment = EnrolmentDTO(
        id=1,
        user_id="user123",
        course_id=1,
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PAID,
    )
    mock_get.return_value = enrolment
    resp = client.get(f"/api/enrolment/1/details", query_string={"user_id": "user123"}, headers=user_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 1

    mock_get.assert_called_once_with(EnrolmentByUserDTO(enrolment_id=1, user_id="user123"))
    mock_user.assert_called_once()

@patch("webapp.api.enrolments.routes.EnrolmentService.get_active")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_get_active(
        mock_admin: MagicMock,
        mock_get: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str]
) -> None:
    mock_admin.return_value = MagicMock(id="admin123", role="admin")
    enrolment = [EnrolmentDTO(
        id=1,
        user_id="admin123",
        course_id=1,
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PAID)]

    mock_get.return_value = enrolment
    resp = client.get(f"/api/enrolment/active", headers=admin_headers)
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["enrolments"][0]["user_id"] == "admin123"

    mock_admin.assert_called_once()
    mock_get.assert_called_once()

@patch("webapp.api.enrolments.routes.EnrolmentService.delete_by_id")
@patch("webapp.api.auth.decorators.UserService.get_user_by_id")
def test_delete_by_id(
        mock_admin: MagicMock,
        mock_get: MagicMock,
        client: FlaskClient,
        admin_headers: dict[str, str]
) -> None:
    mock_admin.return_value = MagicMock(id="admin123", role="admin")
    enrolment = DeleteEnrolmentDTO(
        enrolment_id=1
    )
    mock_get.return_value = enrolment
    resp = client.delete(f"/api/enrolment/{enrolment.enrolment_id}", headers=admin_headers)

    assert resp.status_code == 204
    data = resp.get_json()
    assert data is None
    mock_admin.assert_called_once()
    mock_get.assert_called_once_with(DeleteEnrolmentDTO(1))









