from datetime import datetime, timezone

from sqlalchemy import select, and_, update

from webapp.database.models.enrolments import Enrolment, Status
from webapp.database.repositories.generic import GenericRepository
from webapp.extensions import db


class EnrolmentRepository(GenericRepository[Enrolment]):
    def __init__(self) -> None:
        super().__init__(Enrolment)

    def get_by_user_and_course(self, course_id: int, user_id: str) -> Enrolment | None:
        stmt = select(Enrolment).where(and_(Enrolment.course_id == course_id, Enrolment.user_id == user_id))
        return db.session.scalars(stmt).first()

    def get_by_id(self, enrolment_id: int) -> Enrolment | None:
        stmt = select(Enrolment).where(Enrolment.id == enrolment_id)
        return db.session.scalars(stmt).first()

    def get_active(self) -> list[Enrolment]:
        stmt = select(Enrolment).where(Enrolment.status == Status.ACTIVE)
        return list(db.session.scalars(stmt).all())

    def mark_expired_enrolments_completed(self) -> list[Enrolment]:
        update_stmt = (
            update(Enrolment)
            .where(
                Enrolment.course_end_date < datetime.now(timezone.utc),
                Enrolment.status == Status.ACTIVE
            )
            .values(status=Status.COMPLETED)
        )
        db.session.execute(update_stmt)
        db.session.commit()

        stmt = select(Enrolment).where(
            Enrolment.status == Status.COMPLETED,
            Enrolment.course_end_date < datetime.now(timezone.utc)
        )
        return list(db.session.scalars(stmt).all())