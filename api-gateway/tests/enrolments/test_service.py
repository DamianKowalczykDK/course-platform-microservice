from typing import Generator
from unittest.mock import patch, MagicMock

import pytest
from flask import Flask

from webapp.services.enrolments.dtos import CreateEnrolmentDTO, EnrolmentIdDTO, EnrolmentByUserDTO, DeleteEnrolmentDTO
from webapp.services.enrolments.services import EnrolmentService


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        "ENROLMENT_SERVICE_URL": "http://localhost:enrolment-service-webapp"
    })
    return app

@pytest.fixture
def service(app: Flask) -> Generator[EnrolmentService, None, None]:
    with app.app_context():
        yield EnrolmentService()


@patch("webapp.services.enrolments.services.httpx.post")
@patch("webapp.services.enrolments.services.raise_for_status")
def test_create_enrolment(
        mock_raise: MagicMock,
        mock_post: MagicMock,
        service: EnrolmentService,
        app: Flask
) -> None:
    dto = CreateEnrolmentDTO(
        course_id=1,
        user_id="123"
    )
    mock_raise.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "id":1,
        "user_id": "123",
        "course_id":1,
        "status": "active",
        "payment_status":"pending"
    }

    with app.app_context():
        service.create_enrolment_for_user(dto)

    mock_post.assert_called_once()
    sent_payload = mock_post.call_args.kwargs["json"]
    assert sent_payload["course_id"] == 1
    assert sent_payload["user_id"] == "123"

@patch("webapp.services.enrolments.services.httpx.patch")
@patch("webapp.services.enrolments.services.raise_for_status")
def test_set_paid(mock_raise: MagicMock, mock_patch: MagicMock, service: EnrolmentService, app: Flask) -> None:
    dto = EnrolmentIdDTO(1)
    mock_patch.return_value.json.return_value = {
        "id": 1,
        "user_id": "123",
        "course_id": 1,
        "status": "complete",
        "payment_status": "pending"
    }
    mock_raise.return_value.status_code = 200

    with app.app_context():
        service.set_paid(dto)

    mock_patch.assert_called_once()
    sent_payload = mock_patch.call_args.kwargs["json"]
    assert sent_payload["enrolment_id"] == 1

@patch("webapp.services.enrolments.services.httpx.patch")
@patch("webapp.services.enrolments.services.raise_for_status")
def test_expired_courses(mock_raise: MagicMock, mock_patch: MagicMock, service: EnrolmentService, app: Flask) -> None:
    mock_patch.return_value.json.return_value = {
        "enrolments":[{
            "id": 1,
            "user_id": "123",
            "course_id": 1,
            "status": "complete",
            "payment_status": "paid"
        }]
    }
    mock_raise.return_value.status_code = 200

    with app.app_context():
        result = service.expired_courses()

    mock_patch.assert_called_once()
    mock_raise.assert_called_once()
    assert len(result) == 1
    assert result[0].payment_status == "paid"

@patch("webapp.services.enrolments.services.httpx.get")
@patch("webapp.services.enrolments.services.raise_for_status")
def test_get_by_id(mock_raise: MagicMock, mock_get: MagicMock, service: EnrolmentService, app: Flask) -> None:
    dto = EnrolmentIdDTO(1)
    mock_get.return_value.json.return_value = {
            "id": 1,
            "user_id": "123",
            "course_id": 1,
            "status": "complete",
            "payment_status": "paid"
        }
    mock_raise.return_value.status_code = 200
    with app.app_context():
        result = service.get_by_id(dto)
    mock_get.assert_called_once()
    mock_raise.assert_called_once()

    assert result.user_id == "123"

@patch("webapp.services.enrolments.services.httpx.get")
@patch("webapp.services.enrolments.services.raise_for_status")
def test_get_by_id_and_user(mock_raise: MagicMock, mock_get: MagicMock, service: EnrolmentService, app: Flask) -> None:
    dto = EnrolmentByUserDTO(
        enrolment_id=1,
        user_id="123"
    )
    mock_get.return_value.json.return_value = {"id": 1,
            "user_id": "123",
            "course_id": 1,
            "status": "complete",
            "payment_status": "paid"
        }
    mock_raise.return_value.status_code = 200
    with app.app_context():
        result = service.get_by_id_and_user(dto)
    mock_get.assert_called_once_with(
        "http://localhost:enrolment-service-webapp/1/details",
        params={"user_id": dto.user_id},
        timeout=5
    )
    mock_raise.assert_called_once()

    assert result.user_id == "123"

@patch("webapp.services.enrolments.services.httpx.get")
@patch("webapp.services.enrolments.services.raise_for_status")
def test_get_active(mock_raise: MagicMock, mock_get: MagicMock, service: EnrolmentService, app: Flask) -> None:
    mock_get.return_value.json.return_value = {
        "enrolments": [{"id": 1,
        "user_id": "123",
        "course_id": 1,
        "status": "complete",
        "payment_status": "paid"
       }]
       }
    mock_raise.return_value.status_code = 200
    with app.app_context():
        result = service.get_active()

    mock_get.assert_called_once_with("http://localhost:enrolment-service-webapp/active", timeout=5)
    mock_raise.assert_called_once()

    assert len(result) == 1
    assert result[0].user_id == "123"

@patch("webapp.services.enrolments.services.httpx.delete")
@patch("webapp.services.enrolments.services.raise_for_status")
def test_delete_by_id(mock_raise: MagicMock, mock_del: MagicMock, service: EnrolmentService, app: Flask) -> None:
    dto = DeleteEnrolmentDTO(enrolment_id=1)
    mock_del.return_value.json.return_value = {"uid": 1}
    mock_raise.return_value.status_code = 204

    with app.app_context():
        service.delete_by_id(dto)
    mock_del.assert_called_once_with("http://localhost:enrolment-service-webapp/1", timeout=5)
    mock_raise.assert_called_once()







