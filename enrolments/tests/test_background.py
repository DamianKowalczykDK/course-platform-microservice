from unittest.mock import MagicMock, patch
from webapp.background import start_enrolment_expiration_job
from flask import Flask
import pytest


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def container() -> MagicMock:
    mock_container = MagicMock()
    mock_enrolment_service = MagicMock()
    mock_enrolment_service.return_value = mock_container
    return mock_container

@patch("webapp.background.BackgroundScheduler")
def test_start_job_initialization(mock_scheduler_es: MagicMock, container: MagicMock, app: Flask) -> None:
    mock_scheduler = MagicMock()
    mock_scheduler_es.return_value = mock_scheduler

    with app.app_context():
        start_enrolment_expiration_job(app, container)

    mock_scheduler.add_job.assert_called_once()
    mock_scheduler_es.assert_called_once()

@patch("webapp.background.BackgroundScheduler")
def test_start_expiration_jobs(mock_scheduler_es: MagicMock, container: MagicMock, app: Flask) -> None:
    mock_scheduler = MagicMock()
    mock_scheduler_es.return_value = mock_scheduler

    with app.app_context():
        start_enrolment_expiration_job(app, container)

        job_fn = mock_scheduler.add_job.call_args[0][0]
        job_fn()

    enrolment = container.enrolment_service.return_value
    enrolment.expired_courses.assert_called_once()


