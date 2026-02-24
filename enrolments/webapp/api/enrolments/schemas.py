from pydantic import BaseModel, Field
from webapp.database.models.enrolments import PaymentStatus, Status

class CreateEnrolmentSchema(BaseModel):
    """
    Schema for creating a new enrolment.

    Attributes:
        course_id (int): The ID of the course to enrol in.
        user_id (str): The unique identifier of the user enrolling. Minimum length 1.
    """
    course_id: int
    user_id: str = Field(..., min_length=1)


class EnrolmentResponseSchema(BaseModel):
    """
    Schema representing a single enrolment in API responses.

    Attributes:
        id (int): The unique ID of the enrolment.
        course_id (int): The ID of the enrolled course.
        user_id (str): The ID of the user enrolled in the course.
        status (Status): The current status of the enrolment (ACTIVE, CANCELED, COMPLETED).
        payment_status (PaymentStatus): The payment status (PENDING, PAID, FAILED).
        invoice_url (str | None): Optional URL of the invoice if payment has been made.
    """
    id: int
    course_id: int
    user_id: str
    status: Status
    payment_status: PaymentStatus
    invoice_url: str | None = None


class EnrolmentsListResponseSchema(BaseModel):
    """
    Schema for returning a list of enrolments.

    Attributes:
        enrolments (list[EnrolmentResponseSchema]): List of enrolment objects.
    """
    enrolments: list[EnrolmentResponseSchema]


class EnrolmentIdSchema(BaseModel):
    """
    Schema for identifying a single enrolment by ID.

    Attributes:
        enrolment_id (int): The unique ID of the enrolment.
    """
    enrolment_id: int


class EnrolmentByUserSchema(BaseModel):
    """
    Schema for identifying a single enrolment by user and enrolment ID.

    Attributes:
        enrolment_id (int): The unique ID of the enrolment.
        user_id (str): The ID of the user associated with the enrolment.
    """
    enrolment_id: int
    user_id: str


class DeleteEnrolmentSchema(BaseModel):
    """
    Schema for deleting an enrolment by ID.

    Attributes:
        enrolment_id (int): The unique ID of the enrolment to delete.
    """
    enrolment_id: int