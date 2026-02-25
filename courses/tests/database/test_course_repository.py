from datetime import datetime
from sqlalchemy.orm import Session
from webapp.database.models.courses import Course
from webapp.database.repositories.courses import CourseRepository



def test_get_by_id_when_not_found(session: Session) -> None:
    repo = CourseRepository()

    course_a = repo.get_by_id(999)
    assert course_a is None

def test_get_by_id_when_found_course(session: Session, course: Course) -> None:
    session.add(course)
    repo = CourseRepository()
    course_a = repo.get_by_id(1)

    assert course_a is not None
    assert course_a.name == "Test"
    assert course_a.description == "test"

def test_get_by_name(session: Session, course: Course) -> None:
    session.add(course)
    repo = CourseRepository()
    course_a = repo.get_by_name("Test")

    assert course_a is not None
    assert course_a[0].name == "Test"
    assert course_a[0].id == 1

def test_delete_by_id(session: Session, course: Course) -> None:
    session.add(course)
    repo = CourseRepository()
    course_a = repo.get_by_id(1)
    assert course_a is not None
    repo.delete_by_id(1)
    course_a = repo.get_by_id(1)
    assert course_a is None

def test_update(session: Session, course: Course) -> None:
    session.add(course)
    repo = CourseRepository()
    course.update(
        {
            "name": "Test1",
            "description": "test",
            "price":100,
            "start_date":datetime(2026, 1, 1),
            "end_date":datetime(2026, 1, 2),
        }
    )
    repo.get_by_id(1)
    assert course.name == "Test1"
    assert repr(course) == f"Course id: 1 tittle: Test1"






