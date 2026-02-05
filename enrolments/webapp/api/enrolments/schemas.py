from pydantic import BaseModel, Field


class CreateEnrolmentSchema(BaseModel):
    course_id: int
    user_id: str = Field(..., min_length=1)

class EnrolmentResponseSchema(BaseModel):
    id: int
    course_id: int
    user_id: str
    invoice_url: str | None = None

class EnrolmentIdSchema(BaseModel):
    enrolment_id: int
