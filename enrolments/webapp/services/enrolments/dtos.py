from webapp.database.models.enrolments import PaymentStatus, Status
from dataclasses import dataclass

@dataclass(frozen=True)
class CreateEnrolmentDTO:
    """
    Data transfer object for creating a new enrolment.

    Attributes:
        user_id (str): The ID of the user enrolling in a course.
        course_id (int): The ID of the course to enroll in.
    """
    user_id: str
    course_id: int

@dataclass(frozen=True)
class ReadEnrolmentDTO:
    """
    Data transfer object for reading enrolment details.

    Attributes:
        id (int): Enrolment ID.
        user_id (str): ID of the enrolled user.
        course_id (int): ID of the course.
        status (Status): Current status of the enrolment (ACTIVE, CANCELED, COMPLETED).
        payment_status (PaymentStatus): Payment status (PENDING, PAID, FAILED).
        invoice_url (str | None): Optional URL to the invoice.
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
    DTO for referencing an enrolment by its ID.

    Attributes:
        enrolment_id (int): The enrolment's primary key.
    """
    enrolment_id: int

@dataclass(frozen=True)
class EnrolmentByUserDTO:
    """
    DTO for referencing an enrolment by ID and user ID.

    Attributes:
        enrolment_id (int): The enrolment's primary key.
        user_id (str): The user's ID.
    """
    enrolment_id: int
    user_id: str

@dataclass(frozen=True)
class DeleteEnrolmentDTO:
    """
    DTO for deleting an enrolment.

    Attributes:
        enrolment_id (int): The enrolment's primary key to delete.
    """
    enrolment_id: int