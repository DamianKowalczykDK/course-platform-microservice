from webapp.database.models.enrolments import PaymentStatus, Status
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateEnrolmentDTO:
    user_id: str
    course_id: int

@dataclass(frozen=True)
class ReadEnrolmentDTO:
    id: int
    user_id: str
    course_id: int
    status: Status
    payment_status: PaymentStatus
    invoice_url: str | None = None


@dataclass(frozen=True)
class EnrolmentIdDTO:
    enrolment_id: int
