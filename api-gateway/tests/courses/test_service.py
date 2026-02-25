from typing import Generator
from unittest.mock import patch, MagicMock

import httpx
from flask import Flask, Response
import pytest

from webapp.services.courses.dtos import CreateCourseDTO, CourseDTO, CourseIdDTO, CourseNameDTO, UpdateCourseDTO
from webapp.services.courses.services import CourseService


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        "COURSE_SERVICE_URL": "https://localhost:courses-webapp",
        "HTTP_TIMEOUT": 5,
    }
    )
    return app
@pytest.fixture
def service(app: Flask) -> Generator[CourseService, None, None]:
    with app.app_context():
        yield CourseService()

def make_response(json_data: dict, status_code: int = 200) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.json.return_value = json_data
    resp.status_code = status_code
    return resp

@patch("webapp.services.courses.services.httpx.post")
@patch("webapp.services.courses.services.raise_for_status")
def test_create_course(mock_raise: MagicMock, mock_post: MagicMock, service: CourseService, app: Flask) -> None:
    dto = CreateCourseDTO(
        name="Test",
        description="Test",
        price=100,
        start_date="2026-01-10",
        end_date="2026-01-11"
    )
    mock_post.return_value = make_response({
        "id": 1,
        "name": "Test",
        "description": "Test",
        "price": 100,
        "start_date": "2026-01-10",
        "end_date": "2026-01-11",
        "max_participants": 10
    }, 201)

    with app.app_context():
        result = service.create_course(dto)

    assert isinstance(result, CourseDTO)
    mock_raise.assert_called_once()
    mock_post.assert_called_once()

@patch("webapp.services.courses.services.httpx.get")
@patch("webapp.services.courses.services.raise_for_status")
def test_get_by_id(mock_raise: MagicMock, mock_get: MagicMock, service: CourseService, app: Flask) -> None:
    dto = CourseIdDTO(1)
    mock_get.return_value = make_response({
        "id": 1,
        "name": "Test",
        "description": "Test",
        "price": 100,
        "start_date": "2026-01-10",
        "end_date": "2026-01-11",
        "max_participants": 10
    }
    )

    with app.app_context():
        result = service.get_by_id(dto)

    assert result.id == 1
    mock_raise.assert_called_once()
    mock_get.assert_called_once_with("https://localhost:courses-webapp/1", timeout=5)

@patch("webapp.services.courses.services.httpx.get")
def test_get_by_name(mock_get: MagicMock, service: CourseService, app: Flask) -> None:
    dto = CourseNameDTO("Test")
    mock_get.return_value.json.return_value = {
        "courses": [
            {
            "id": 1,
            "name": "Test",
            "description": "Test",
            "price": 100,
            "start_date": "2026-01-10",
            "end_date": "2026-01-11",
            "max_participants": 10
        }]
    }

    with app.app_context():
        result = service.get_by_name(dto)

    assert len(result) == 1
    assert result[0].name == "Test"
    mock_get.assert_called_once_with("https://localhost:courses-webapp/", params={"name": "Test"}, timeout=5)

@patch("webapp.services.courses.services.httpx.patch")
@patch("webapp.services.courses.services.raise_for_status")
def test_update_course(mock_raise: MagicMock, mock_patch: MagicMock, service: CourseService, app: Flask) -> None:
    dto = UpdateCourseDTO(1)
    mock_patch.return_value = make_response({
        "id": 1,
        "name": "Test",
        "description": "Test",
        "price": 100,
        "start_date": "2026-01-10",
        "end_date": "2026-01-11",
        "max_participants": 10
    })
    with app.app_context():
        result = service.update_course(dto)

    assert result.id == 1
    mock_raise.assert_called_once()
    mock_patch.assert_called_once_with("https://localhost:courses-webapp/1", json=dto.__dict__, timeout=5)

@patch("webapp.services.courses.services.httpx.delete")
@patch("webapp.services.courses.services.raise_for_status")
def test_delete_course(mock_raise: MagicMock, mock_delete: MagicMock, service: CourseService, app: Flask) -> None:
    dto = CourseIdDTO(1)
    mock_delete.return_value = make_response({}, 204)
    with app.app_context():
        service.delete_by_id(dto)

    mock_raise.assert_called_once()
    mock_delete.assert_called_once_with("https://localhost:courses-webapp/1", timeout=5)