from sqlalchemy.orm import Session
from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.database.models.enrolments import Enrolment, Status


def test_get_by_in_when_found_course(session: Session, enrolment: Enrolment) -> None:
    session.add(enrolment)
    repo = EnrolmentRepository()
    result = repo.get_by_id(1)

    assert result is not None
    assert result.course_id == 1
    assert result.status == Status.ACTIVE

def test_get_by_user_and_course_success(session: Session, enrolment: Enrolment) -> None:
    session.add(enrolment)
    repo = EnrolmentRepository()
    result = repo.get_by_user_and_course(1, "123")
    assert result is not None

    assert result.course_id == 1
    assert result.status == Status.ACTIVE
    assert result.user_id == "123"
    assert result.__repr__() == "Enrolment(id=1, course_id=1)"

def test_get_by_active(session: Session, enrolment: Enrolment) -> None:
    session.add(enrolment)
    repo = EnrolmentRepository()
    result = repo.get_active()
    assert result is not None

    enrolment_a = result[0]
    assert enrolment_a.user_id == "123"







