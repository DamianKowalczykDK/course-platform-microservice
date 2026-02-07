from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.database.repositories.generic import GenericRepository
from webapp.database.models.enrolments import Enrolment
from sqlalchemy.orm import Session

def test_generic_add_get_all_delete(session: Session, enrolment: Enrolment) -> None:
    repo = GenericRepository(Enrolment)
    repo.add(enrolment)
    repo.flush()
    assert enrolment.user_id == "123"

    enrolment_a = repo.get(1)
    assert enrolment_a is not None
    assert enrolment_a.user_id == "123"

    repo.add_all([enrolment])
    repo.commit()
    assert enrolment.user_id == "123"

    repo.get_all()
    assert enrolment.course_id == 1

    repo.delete(enrolment)
    repo.commit()
    enrolment_a = repo.get(1)
    assert enrolment_a is None

def test_rollback_refresh_delete_by_id(session: Session, enrolment: Enrolment) -> None:
    repo = GenericRepository(Enrolment)
    repo.add_and_commit(enrolment)

    enrolment_a = repo.get(1)
    assert enrolment_a is not None

    repo.rollback()
    repo.refresh(enrolment)

    assert enrolment.user_id == "123"
    repo.delete_by_id(1)
    repo.commit()

    enrolment_a = repo.get(1)
    assert enrolment_a is None

def test_delete_and_commit(session: Session, enrolment: Enrolment) -> None:
    repo = GenericRepository(Enrolment)
    repo.add_and_commit(enrolment)

    enrolment_a = repo.get(1)
    assert enrolment_a is not None
    assert enrolment_a.user_id == "123"

    repo.delete_and_commit(enrolment)
    assert repo.get(1) is None





