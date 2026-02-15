from sqlalchemy.orm import Session
from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.database.models.enrolments import Enrolment, Status, PaymentStatus
import datetime

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
    result = repo.get_by_id_and_user(1, "123")
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

def test_mark_expired_enrolments_completed(session: Session) -> None:
    enrolment_expired = Enrolment(
        course_id=1,
        user_id="123",
        invoice_url="http://invoice.example.com/555",
        status=Status.ACTIVE,
        payment_status=PaymentStatus.PENDING,
        course_end_date=datetime.datetime(2026, 1, 25),
    )
    session.add(enrolment_expired)
    repo = EnrolmentRepository()
    result = repo.mark_expired_enrolments_completed()

    assert len(result) == 1
    assert result[0].status.value == "completed"












