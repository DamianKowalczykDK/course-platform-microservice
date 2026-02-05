from sqlalchemy import select, and_
from webapp.database.models.enrolments import Enrolment
from webapp.database.repositories.generic import GenericRepository
from webapp.extensions import db

class EnrolmentRepository(GenericRepository[Enrolment]):
    def __init__(self) -> None:
        super().__init__(Enrolment)

    def get_by_user_and_course(self, course_id: int, user_id: int) -> Enrolment | None:
        stmt = select(Enrolment).where(and_(Enrolment.course_id == course_id, Enrolment.user_id == user_id))
        return db.session.scalars(stmt).first()

    def get_by_id(self, enrolment_id: int) -> Enrolment | None:
        stmt = select(Enrolment).where(Enrolment.id == enrolment_id)
        return db.session.scalars(stmt).first()

