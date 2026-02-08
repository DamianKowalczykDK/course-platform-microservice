from webapp.database.repositories.generic import GenericRepository
from webapp.database.repositories.courses import CourseRepository
from webapp.database.models.courses import Course
from sqlalchemy.orm import Session
import pytest

def test_generic_add_get_all_delete(session: Session, course: Course) -> None:
    repo = GenericRepository(Course)
    repo.add(course)
    repo.flush()
    assert course.name is not None

    course_a = repo.get(1)
    assert course_a is not None
    assert course_a.name == "Test"

    repo.add_all([course])
    repo.flush()
    assert course.id is not None

    repo.get_all()
    assert course.description == "test"

    repo.delete(course)
    repo.flush()
    assert repo.get(1) is None


def test_generic_commit_rollback_refresh_delete_by_id(session: Session, course: Course) -> None:
    repo = GenericRepository(Course)
    repo.add_and_commit(course)
    assert course.id is not None

    course.name = "Test1"
    repo.rollback()
    repo.refresh(course)

    assert course.name == "Test"

    repo.delete_by_id(1)
    repo.commit()
    assert repo.get(1) is None

def test_generic_delete_and_commit(session: Session, course: Course) -> None:
    repo = GenericRepository(Course)
    repo.add_and_commit(course)
    assert course.id is not None
    repo.delete_and_commit(course)
    assert repo.get(1) is None



