from webapp.services.enrolments.dtos import ReadEnrolmentDTO
from webapp.database.models.enrolments import Enrolment

def to_read_dto(model: Enrolment) -> ReadEnrolmentDTO:
    return ReadEnrolmentDTO(
        id=model.id,
        course_id=model.course_id,
        user_id=model.user_id,
        invoice_url=model.invoice_url,
    )