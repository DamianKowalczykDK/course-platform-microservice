from datetime import datetime, timezone
from sqlalchemy import select, and_
from webapp.database.models.enrolments import Enrolment, Status
from webapp.database.repositories.generic import GenericRepository
from webapp.extensions import db


class EnrolmentRepository(GenericRepository[Enrolment]):
    """
    Repository class for performing database operations on Enrolment objects.

    Inherits from GenericRepository and provides custom methods for querying
    enrolments by user, status, or expiry.

    Methods:
        get_by_id_and_user(enrolment_id, user_id) -> Enrolment | None
        get_by_id(enrolment_id) -> Enrolment | None
        get_active() -> list[Enrolment]
        mark_expired_enrolments_completed() -> list[Enrolment]
    """

    def __init__(self) -> None:
        """Initialize the repository with the Enrolment model."""
        super().__init__(Enrolment)

    def get_by_id_and_user(self, enrolment_id: int, user_id: str) -> Enrolment | None:
        """
        Retrieve an enrolment by its ID and associated user ID.

        Args:
            enrolment_id (int): The ID of the enrolment.
            user_id (str): The ID of the user.

        Returns:
            Enrolment | None: The matching enrolment, or None if not found.
        """
        stmt = select(Enrolment).where(and_(Enrolment.id == enrolment_id, Enrolment.user_id == user_id))
        return db.session.scalars(stmt).first()

    def get_by_id(self, enrolment_id: int) -> Enrolment | None:
        """
        Retrieve an enrolment by its ID.

        Args:
            enrolment_id (int): The ID of the enrolment.

        Returns:
            Enrolment | None: The matching enrolment, or None if not found.
        """
        stmt = select(Enrolment).where(Enrolment.id == enrolment_id)
        return db.session.scalars(stmt).first()

    def get_active(self) -> list[Enrolment]:
        """
        Retrieve all enrolments with ACTIVE status.

        Returns:
            list[Enrolment]: A list of active enrolments.
        """
        stmt = select(Enrolment).where(Enrolment.status == Status.ACTIVE)
        return list(db.session.scalars(stmt).all())

    def mark_expired_enrolments_completed(self) -> list[Enrolment]:
        """
        Mark all enrolments whose course_end_date has passed and are still ACTIVE as COMPLETED.

        Returns:
            list[Enrolment]: The list of enrolments that were updated to COMPLETED.
        """
        now = datetime.now(timezone.utc)

        to_expire = db.session.scalars(
            select(Enrolment).where(
                Enrolment.course_end_date < now,
                Enrolment.status == Status.ACTIVE
            )
        ).all()

        for e in to_expire:
            e.status = Status.COMPLETED

        return list(to_expire)