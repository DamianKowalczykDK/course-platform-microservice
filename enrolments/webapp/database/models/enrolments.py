from sqlalchemy import Integer, String, DateTime, UniqueConstraint, Enum, func
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from webapp.extensions import db
from enum import Enum as PyEnum

class Status(PyEnum):
    """Enumeration of possible enrolment statuses."""
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"

class PaymentStatus(PyEnum):
    """Enumeration of possible payment statuses for an enrolment."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class Enrolment(db.Model):  # type: ignore
    """
    Represents an enrolment of a user in a course.

    Attributes:
        id (int): Primary key of the enrolment.
        course_id (int): ID of the course.
        user_id (str): ID of the user.
        invoice_url (str | None): URL to the payment invoice, if any.
        status (Status): Status of the enrolment (ACTIVE, CANCELED, COMPLETED).
        payment_status (PaymentStatus): Status of the payment (PENDING, PAID, FAILED).
        created_at (datetime): Timestamp of when the enrolment was created.
        updated_at (datetime): Timestamp of the last update to the enrolment.
        course_end_date (datetime | None): End date of the course for this enrolment.

    Table constraints:
        UniqueConstraint: Ensures that a user cannot enrol in the same course more than once.
    """

    __tablename__ = "enrolments"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_enrolments"), )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    invoice_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default=Status.ACTIVE)
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    course_end_date: Mapped[datetime] = mapped_column(DateTime,  nullable=True)

    def __repr__(self) -> str:
        """Return a human-readable representation of the enrolment."""
        return f"Enrolment(id={self.id}, course_id={self.course_id})"