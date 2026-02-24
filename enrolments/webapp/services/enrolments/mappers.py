from webapp.services.enrolments.dtos import ReadEnrolmentDTO
from webapp.database.models.enrolments import Enrolment

def to_read_dto(model: Enrolment) -> ReadEnrolmentDTO:
    """
    Map an Enrolment SQLAlchemy model instance to a ReadEnrolmentDTO.

    Args:
        model (Enrolment): The Enrolment model instance.

    Returns:
        ReadEnrolmentDTO: The corresponding DTO with enrolment details.
    """
    return ReadEnrolmentDTO(
        id=model.id,
        course_id=model.course_id,
        user_id=model.user_id,
        status=model.status,
        payment_status=model.payment_status,
        invoice_url=model.invoice_url,
    )