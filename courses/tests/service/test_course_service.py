from datetime import datetime
from unittest.mock import MagicMock
from webapp.database.models.courses import Course
from webapp.services.courses.dtos import CreateCourseDTO, CourseIdDTO, ReadCourseDTO, CourseNameDTO, UpdateCourseDTO
from webapp.services.courses.services import CourseService
from webapp.services.exceptions import ConflictException, NotFoundException, ValidationException
from sqlalchemy.exc import IntegrityError
from flask import Flask
import pytest



@pytest.fixture
def mock_course_repository() -> MagicMock:
    return MagicMock()

@pytest.fixture
def flask_app() -> Flask:
    app = Flask(__name__)
    return app

@pytest.fixture
def course_service(mock_course_repository: MagicMock) -> CourseService:
    return CourseService(course_repository=mock_course_repository)

def test_create_course(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    dto = CreateCourseDTO(
        name="Test",
        description="test",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2)
    )
    mock_course_repository.get_by_name.return_value = None
    course_service.create_course(dto)

    mock_course_repository.get_by_name.assert_called_with("Test")
    saved_course = mock_course_repository.add_and_commit.call_args[0][0]
    assert saved_course.name == "Test"
    assert saved_course.description == "test"

def test_create_course_if_already_exists(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    dto = CreateCourseDTO(
        name="Test",
        description="test",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2)
    )
    mock_course_repository.get_by_name.return_value = dto
    with pytest.raises(ConflictException, match="Course already exists"):
        course_service.create_course(dto)
        mock_course_repository.get_by_name.assert_called_once()

def test_create_course_if_integrity_error(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    dto = CreateCourseDTO(
        name="Test",
        description="test",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2)
    )
    mock_course_repository.get_by_name.return_value = None
    mock_course_repository.add_and_commit.side_effect = IntegrityError(None, None, BaseException())

    course_service.create_course(dto)
    mock_course_repository.rollback.assert_called_once()


def test_get_by_id(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    dto = ReadCourseDTO(
        id=1,
        name="Test",
        description="test",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2)
    )
    mock_course_repository.get_by_id.return_value = dto
    dto_id = CourseIdDTO(course_id=1)
    course = course_service.get_by_id(dto_id)
    assert course.id == 1
    assert course.name == "Test"

def test_get_by_id_if_not_found(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    mock_course_repository.get_by_id.return_value = None
    with pytest.raises(NotFoundException, match="Course not found"):
        dto = CourseIdDTO(course_id=1)
        course_service.get_by_id(dto)
        mock_course_repository.get_by_id.assert_called_once()


def test_get_by_name(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    dto = ReadCourseDTO(
        id=1,
        name="Test",
        description="test",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2)
    )
    mock_course_repository.get_by_name.return_value = dto
    dto_name = CourseNameDTO(name="Test")
    course = course_service.get_by_name(dto_name)
    assert course.name == "Test"

def test_get_by_name_if_not_found(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    mock_course_repository.get_by_name.return_value = None
    with pytest.raises(NotFoundException, match="Course not found"):
        dto = CourseNameDTO(name="Test")
        course_service.get_by_name(dto)
        mock_course_repository.get_by_name.assert_called_once()

def test_update_course(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    course = Course(
        name="Test",
        description="test",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2),
        )

    updated_dto = UpdateCourseDTO(
        id=1,
        name="Test",
        description="test1",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2)
    )
    mock_course_repository.get_by_id.return_value = course
    course_service.update_course(updated_dto)
    mock_course_repository.add_and_commit.assert_called_once()

def test_update_if_not_found(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    mock_course_repository.get_by_id.return_value = None
    with pytest.raises(NotFoundException, match="Course not found"):
        dto = UpdateCourseDTO(
            id=1,
            name="Test",
            description="test1",
            price=100,
            start_date=datetime(2026, 1, 1),
            end_date=datetime(2026, 1, 2)
        )
        course_service.update_course(dto)
        mock_course_repository.get_by_name.assert_called_once()

def test_delete_by_id(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    dto = ReadCourseDTO(
        id=1,
        name="Test",
        description="test",
        price=100,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 2)
    )
    mock_course_repository.get_by_id.return_value = dto
    dto_id = CourseIdDTO(course_id=1)
    course_service.delete_by_id(dto_id)
    mock_course_repository.delete_and_commit.assert_called_once()

def test_delete_by_id_if_not_found(mock_course_repository: MagicMock, course_service: CourseService) -> None:
    mock_course_repository.get_by_id.return_value = None
    with pytest.raises(NotFoundException, match="Course not found"):
        dto = CourseIdDTO(course_id=1)
        course_service.delete_by_id(dto)
        mock_course_repository.delete_and_commit.assert_called_once()




