from pydantic import BaseModel
from webapp.services.enrolments.dtos import PaymentStatus, Status


class CreateEnrolmentSchema(BaseModel):
    course_id: int

class EnrolmentResponseSchema(BaseModel):
    id: int
    course_id: int
    user_id: str
    status: Status
    payment_status: PaymentStatus
    invoice_url: str | None = None

class EnrolmentIdSchema(BaseModel):
    enrolment_id: int

class EnrolmentByUserSchema(BaseModel):
    enrolment_id: int