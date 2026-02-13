from webapp import register_error_handlers
from webapp.services.enrolments.dtos import ReadEnrolmentDTO, CreateEnrolmentDTO, EnrolmentIdDTO, EnrolmentByUserDTO, \
    DeleteEnrolmentDTO
from webapp.database.models.enrolments import PaymentStatus, Status
from webapp.services.exceptions import ServiceException, ApiException
from webapp.api import api_bp
from webapp.container import Container
from flask import Flask
from flask.testing import FlaskClient
from typing import Generator
from dependency_injector import providers
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    container = Container()
    container.wire(modules=["webapp.api.enrolments.routes"])
    app.container = container #type: ignore
    app.register_blueprint(api_bp)
    register_error_handlers(app)
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def mock_service(app: Flask) -> Generator[MagicMock, None, None]:
    mock = MagicMock()
    app.container.enrolment_service.override(providers.Object(mock))#type: ignore
    yield mock
    app.container.enrolment_service.reset_override()#type: ignore

def test_create_enrolment_success(client: FlaskClient, mock_service: MagicMock) -> None:
    fake_enrolment_dto = ReadEnrolmentDTO(
        id=1,
        user_id="123",
        course_id=1,
        invoice_url="https://invoice.example.com/555",
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PENDING
    )
    create_enrolment = CreateEnrolmentDTO(
        user_id="123",
        course_id=1,
    )

    mock_service.create_enrolment_for_user.return_value = fake_enrolment_dto
    payload = create_enrolment
    response = client.post("/api/enrolment/", json=payload)
    assert response.status_code == 201

def test_create_enrolment_service_exception(client: FlaskClient, mock_service: MagicMock) -> None:
    mock_service.create_enrolment_for_user.side_effect = ServiceException("BOOM")
    create_enrolment = CreateEnrolmentDTO(
        user_id="123",
        course_id=1
    )

    response = client.post("/api/enrolment/", json=create_enrolment)
    assert response.status_code == 500


def test_get_by_id_success(client: FlaskClient, mock_service: MagicMock) -> None:
    fake_enrolment_dto = ReadEnrolmentDTO(
        id=1,
        user_id="123",
        course_id=1,
        invoice_url="https://invoice.example.com/555",
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PENDING
    )
    create_enrolment = CreateEnrolmentDTO(
        user_id="123",
        course_id=1
    )

    mock_service.get_by_id.return_value = fake_enrolment_dto
    response = client.get("/api/enrolment/1", json=create_enrolment)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1



def test_set_paid(client: FlaskClient, mock_service: MagicMock) -> None:
    fake_enrolment_dto = ReadEnrolmentDTO(
        id=1,
        user_id="123",
        course_id=1,
        invoice_url="https://invoice.example.com/555",
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PAID
    )
    enrolment_id = EnrolmentIdDTO(
        enrolment_id=1,
    )

    mock_service.set_paid.return_value = fake_enrolment_dto
    response = client.patch("/api/enrolment/paid", json=enrolment_id)
    assert response.status_code == 200
    data = response.get_json()
    assert data["payment_status"] == PaymentStatus.PAID.value


def test_expired_courses(client: FlaskClient, mock_service: MagicMock) -> None:
    fake_enrolment_dto = ReadEnrolmentDTO(
        id=1,
        user_id="123",
        course_id=1,
        invoice_url="https://invoice.example.com/555",
        status=Status.COMPLETED,
        payment_status=PaymentStatus.PENDING)

    mock_service.expired_courses.return_value = [fake_enrolment_dto]
    response = client.patch("/api/enrolment/expired")
    assert response.status_code == 200

    data = response.get_json()
    assert data["enrolments"][0]["status"] == Status.COMPLETED.value

def test_get_by_id_and_user_success(client: FlaskClient, mock_service: MagicMock) -> None:
    fake_enrolment_dto = ReadEnrolmentDTO(
        id=1,
        user_id="123",
        course_id=1,
        invoice_url="https://invoice.example.com/555",
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PENDING
    )
    enrolment = EnrolmentByUserDTO(
        enrolment_id=1,
        user_id="123"
    )

    mock_service.get_by_id_and_user.return_value = fake_enrolment_dto
    response = client.get(f"/api/enrolment/{enrolment.enrolment_id}/details", query_string={"user_id": enrolment.user_id})
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == enrolment.enrolment_id
    assert data["user_id"] == enrolment.user_id
    mock_service.get_by_id_and_user.assert_called_once()

def test_get_by_id_and_user_if_not_user(client: FlaskClient, mock_service: MagicMock) -> None:
    response = client.get(f"/api/enrolment/1/details")
    assert response.status_code == 400

def test_get_active(client: FlaskClient, mock_service: MagicMock) -> None:
    fake_enrolment_dto = ReadEnrolmentDTO(
            id=1,
            user_id="123",
            course_id=1,
            invoice_url="https://invoice.example.com/555",
            status=Status.ACTIVE,
            payment_status=PaymentStatus.PENDING
    )
    mock_service.get_active.return_value = [fake_enrolment_dto]
    response = client.get(f"/api/enrolment/active")
    assert response.status_code == 200
    data = response.get_json()
    assert data["enrolments"][0]["user_id"] == "123"
    assert data["enrolments"][0]["status"] == Status.ACTIVE.value



def test_delete_by_id(client: FlaskClient, mock_service: MagicMock) -> None:
    enrolment = DeleteEnrolmentDTO(1)
    mock_service.delete_by_id.return_value = enrolment
    response = client.delete(f"/api/enrolment/1")
    assert response.status_code == 204

