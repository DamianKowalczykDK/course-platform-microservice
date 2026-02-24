from enum import Enum
from dataclasses import dataclass

class Status(Enum):
    """
    Enum representing the current status of an enrolment.

    Attributes:
        ACTIVE: The enrolment is active.
        CANCELED: The enrolment has been canceled.
        COMPLETED: The enrolment has been completed.
    """
    ACTIVE = "active"
    CANCELED = "canceled"
    COMPLETED = "completed"


class PaymentStatus(Enum):
    """
    Enum representing the payment status of an enrolment.

    Attributes:
        PENDING: Payment has not been made yet.
        PAID: Payment has been successfully completed.
        FAILED: Payment attempt failed.
    """
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


@dataclass(frozen=True)
class CreateEnrolmentDTO:
    """
    Data required to create a new enrolment for a user in a course.

    Attributes:
        course_id (int): The ID of the course to enrol in.
        user_id (str): The ID of the user enrolling.
    """
    course_id: int
    user_id: str


@dataclass(frozen=True)
class EnrolmentDTO:
    """
    Representation of an enrolment.

    Attributes:
        id (int): Unique ID of the enrolment.
        user_id (str): The ID of the enrolled user.
        course_id (int): The ID of the course.
        status (Status): Current status of the enrolment.
        payment_status (PaymentStatus): Payment status for the enrolment.
        invoice_url (str | None): Optional URL to the invoice for this enrolment.
    """
    id: int
    user_id: str
    course_id: int
    status: Status
    payment_status: PaymentStatus
    invoice_url: str | None = None


@dataclass(frozen=True)
class EnrolmentIdDTO:
    """
    DTO for identifying an enrolment by ID.

    Attributes:
        enrolment_id (int): Unique ID of the enrolment.
    """
    enrolment_id: int


@dataclass(frozen=True)
class EnrolmentByUserDTO:
    """
    DTO for operations requiring both enrolment ID and user ID.

    Attributes:
        enrolment_id (int): Unique ID of the enrolment.
        user_id (str): The ID of the associated user.
    """
    enrolment_id: int
    user_id: str


@dataclass(frozen=True)
class DeleteEnrolmentDTO:
    """
    DTO for deleting an enrolment.

    Attributes:
        enrolment_id (int): Unique ID of the enrolment to delete.
    """
    enrolment_id: int