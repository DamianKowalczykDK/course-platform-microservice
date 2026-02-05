from sqlalchemy import Integer, String, DateTime, UniqueConstraint, Enum, func
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from webapp.extensions import db
from enum import Enum as PyEnum

class Status(PyEnum):
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"

class PaymentStatus(PyEnum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class Enrolment(db.Model): #type: ignore
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

    def __repr__(self) -> str:
        return f"Enrolment(id={self.id}, course_id={self.course_id})"
