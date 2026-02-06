from pydantic import BaseModel, Field

from webapp.database.models.enrolments import PaymentStatus


class CreateEnrolmentSchema(BaseModel):
    course_id: int
    user_id: str = Field(..., min_length=1)

class EnrolmentResponseSchema(BaseModel):
    id: int
    course_id: int
    user_id: str
    payment_status: PaymentStatus
    invoice_url: str | None = None

class EnrolmentIdSchema(BaseModel):
    enrolment_id: int
