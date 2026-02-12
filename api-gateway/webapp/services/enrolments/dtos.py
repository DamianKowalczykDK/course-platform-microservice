from enum import Enum
from dataclasses import dataclass

class Status(Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


@dataclass(frozen=True)
class CreateEnrolmentDTO:
    course_id: int
    user_id: str

@dataclass(frozen=True)
class EnrolmentDTO:
    id: int
    user_id: str
    course_id: int
    status: Status
    payment_status: PaymentStatus
    invoice_url: str | None = None


@dataclass(frozen=True)
class EnrolmentIdDTO:
    enrolment_id: int

@dataclass(frozen=True)
class EnrolmentByUserDTO:
    enrolment_id: int
    user_id: str
