from webapp.services.exceptions import ValidationException, ServiceException, NotFoundException, ConflictException
from webapp.services.enrolments.dtos import CreateEnrolmentDTO, EnrolmentIdDTO
from webapp.services.enrolments.services import EnrolmentService
from webapp.database.models.enrolments import PaymentStatus
from unittest.mock import MagicMock, patch
from typing import Generator
from flask import Flask
import httpx
import pytest


@pytest.fixture(scope='module')
def app() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    app.config['USERS_SERVICE_URL'] = "http://users-service"
    app.config['COURSE_SERVICE_URL'] = "http://course-service"
    app.config["MAIL_DEFAULT_SENDER"] = "default@example.com"
    with app.app_context():
        yield app

@pytest.fixture
def repo() -> MagicMock:
    return MagicMock()

@pytest.fixture
def email_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def service(repo: MagicMock, email_service: MagicMock) -> EnrolmentService:
    service = EnrolmentService(repo, email_service)
    return service

@pytest.fixture
def dto() -> CreateEnrolmentDTO:
    return CreateEnrolmentDTO(user_id="123", course_id=1)

@pytest.fixture
def user_resp() -> MagicMock:
    return MagicMock()

@pytest.fixture
def course_resp() -> MagicMock:
    return MagicMock()

@pytest.fixture
def fake_enrolment() -> MagicMock:
    enrolment = MagicMock()
    enrolment.id = 1
    enrolment.user_id = "123"
    enrolment.course_id = 1
    enrolment.payment_status = PaymentStatus.PENDING
    return enrolment



@patch('webapp.services.enrolments.services.httpx.get')
@patch('webapp.services.enrolments.services.db')
def test_create_enrolment_for_user(
        mock_db: MagicMock,
        mock_get: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        dto: CreateEnrolmentDTO,
) -> None:
    mock_get.return_value.status_code = 200
    mock_db.sesion.begin.return_value.__enter__.return_value = None

    result = service.create_enrolment_for_user(dto)

    assert result.user_id == "123"
    assert result.course_id == 1


@patch('webapp.services.enrolments.services.httpx.get')
def test_create_enrolment_for_course_not_found_user(
        mock_get: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        dto: CreateEnrolmentDTO,
) -> None:
    mock_get.return_value.status_code = 404

    with pytest.raises(ValidationException, match=f"User 123 not found or inactive"):
        service.create_enrolment_for_user(dto)

@patch('webapp.services.enrolments.services.httpx.get')
def test_create_enrolment_for_course_not_found_course(
        mock_get: MagicMock,
        user_resp: MagicMock,
        course_resp: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        dto: CreateEnrolmentDTO,
) -> None:
    user_resp.status_code = 200
    user_resp.json.return_value = {
        "user_id": "123"
    }

    course_resp.status_code = 404

    mock_get.side_effect = [
        user_resp,
        course_resp,
    ]

    with pytest.raises(ValidationException, match=f"Course 1 not found"):
        service.create_enrolment_for_user(dto)


@patch('webapp.services.enrolments.services.httpx.get')
def test_create_enrolment_for_course_http_request_error(
        mock_get: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        dto: CreateEnrolmentDTO
) -> None:
    mock_get.side_effect= httpx.RequestError("Timeout")

    with pytest.raises(ServiceException) as e:
        service.create_enrolment_for_user(dto)

    assert "HTTP Request Error" in str(e.value)

@patch('webapp.services.enrolments.services.httpx.get')
def test_create_enrolment_for_course_service_error(
        mock_get: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        dto: CreateEnrolmentDTO
) -> None:
    mock_get.side_effect= Exception

    with pytest.raises(ServiceException) as e:
        service.create_enrolment_for_user(dto)

    assert "Unknown Server Error: " in str(e.value)

@patch('webapp.services.enrolments.services.httpx.get')
def test_set_paid(
        mock_get: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        fake_enrolment: MagicMock,
) -> None:
    repo.get_by_id.return_value = fake_enrolment

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"email": "test@example.com"}

    _ = service.email_service.send_email

    dto = EnrolmentIdDTO(enrolment_id=1)

    result = service.set_paid(dto)

    assert result.payment_status == PaymentStatus.PAID

def test_set_paid_not_found_exception(
        repo: MagicMock,
        service: EnrolmentService,
) -> None:
    repo.get_by_id.return_value = None

    with pytest.raises(NotFoundException, match="Enrolment not found"):
        dto = EnrolmentIdDTO(enrolment_id=1)
        service.set_paid(dto)

    repo.get_by_id.assert_called_once()

@patch('webapp.services.enrolments.services.httpx.get')
def test_set_paid_conflict_exception(
        mock_get: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        fake_enrolment: MagicMock,
) -> None:

    fake_enrolment.payment_status = PaymentStatus.PAID
    repo.get_by_id.return_value = fake_enrolment

    mock_get.return_value.status_code = 409

    with pytest.raises(ConflictException, match="Enrolment already paid"):
        dto = EnrolmentIdDTO(enrolment_id=1)
        service.set_paid(dto)

    repo.get_by_id.assert_called_once()

@patch('webapp.services.enrolments.services.httpx.get')
def test_set_paid_validation_exception(
        mock_get: MagicMock,
        app: Flask,
        repo: MagicMock,
        service: EnrolmentService,
        fake_enrolment: MagicMock,
) -> None:

    repo.get_by_id.return_value = fake_enrolment
    mock_get.return_value.status_code = 400

    with pytest.raises(ValidationException, match="User not found"):
        dto = EnrolmentIdDTO(enrolment_id=1)
        service.set_paid(dto)

    repo.get_by_id.assert_called_once()


def test_get_by_id(repo: MagicMock,service: EnrolmentService) -> None:
    fake_enrolment =MagicMock()
    service.get_by_id(fake_enrolment)
    assert fake_enrolment is not None
    repo.get_by_id.assert_called_once()

def test_get_by_id_if_not_found_enrolment(repo: MagicMock,service: EnrolmentService) -> None:
    repo.get_by_id.return_value = None
    enrolment_id = EnrolmentIdDTO(1)
    with pytest.raises(NotFoundException, match="Enrolment not found"):
        service.get_by_id(enrolment_id)
    repo.get_by_id.assert_called_once()
