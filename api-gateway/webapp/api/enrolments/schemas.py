from pydantic import BaseModel
from webapp.services.enrolments.dtos import PaymentStatus, Status

class CreateEnrolmentSchema(BaseModel):
    """
    Schema for creating a new enrolment.

    Attributes:
        course_id (int): The ID of the course to enrol the user in.
    """
    course_id: int


class EnrolmentResponseSchema(BaseModel):
    """
    Schema representing a single enrolment response.

    Attributes:
        id (int): Unique enrolment ID.
        course_id (int): ID of the course.
        user_id (str): ID of the enrolled user.
        status (Status): Current status of the enrolment (active, canceled, completed).
        payment_status (PaymentStatus): Payment status of the enrolment (pending, paid, failed).
        invoice_url (str | None): Optional URL to the invoice if payment is completed.
    """
    id: int
    course_id: int
    user_id: str
    status: Status
    payment_status: PaymentStatus
    invoice_url: str | None = None


class EnrolmentsListResponseSchema(BaseModel):
    """
    Schema representing a list of enrolments.

    Attributes:
        enrolments (list[EnrolmentResponseSchema]): List of enrolment responses.
    """
    enrolments: list[EnrolmentResponseSchema]


class EnrolmentIdSchema(BaseModel):
    """
    Schema for identifying a specific enrolment by ID.

    Attributes:
        enrolment_id (int): The unique enrolment ID.
    """
    enrolment_id: int


class EnrolmentByUserSchema(BaseModel):
    """
    Schema for retrieving enrolment details for a specific user.

    Attributes:
        enrolment_id (int): The enrolment ID to retrieve.
    """
    enrolment_id: int


class DeleteEnrolmentSchema(BaseModel):
    """
    Schema for deleting an enrolment.

    Attributes:
        enrolment_id (int): The ID of the enrolment to delete.
    """
    enrolment_id: int