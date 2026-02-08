from webapp.api.enrolments.schemas import CreateEnrolmentSchema, EnrolmentResponseSchema, EnrolmentIdSchema
from webapp.services.enrolments.dtos import CreateEnrolmentDTO, ReadEnrolmentDTO, EnrolmentIdDTO


def to_create_enrolment_dto(schema: CreateEnrolmentSchema) -> CreateEnrolmentDTO:
    return CreateEnrolmentDTO(
        user_id=schema.user_id,
        course_id=schema.course_id,
    )

def to_enrolment_response_schema(dto: ReadEnrolmentDTO) -> EnrolmentResponseSchema:
    return EnrolmentResponseSchema(
        id=dto.id,
        course_id=dto.course_id,
        user_id=dto.user_id,
        status=dto.status,
        payment_status=dto.payment_status,
        invoice_url=dto.invoice_url
    )

def to_enrolment_id_dto(schema: EnrolmentIdSchema) -> EnrolmentIdDTO:
    return EnrolmentIdDTO(enrolment_id=schema.enrolment_id)