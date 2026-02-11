from webapp.services.enrolments.dtos import CreateEnrolmentDTO, EnrolmentDTO, EnrolmentIdDTO
from webapp.api.enrolments.schemas import CreateEnrolmentSchema, EnrolmentResponseSchema, EnrolmentIdSchema


def to_create_enrolment_dto(schema: CreateEnrolmentSchema, user_id: str) -> CreateEnrolmentDTO:
    return CreateEnrolmentDTO(user_id=user_id, course_id=schema.course_id)


def to_enrolment_response_schema(dto: EnrolmentDTO) -> EnrolmentResponseSchema:
    return EnrolmentResponseSchema(
        id=dto.id,
        user_id=dto.user_id,
        course_id=dto.course_id,
        status=dto.status,
        payment_status=dto.payment_status
    )

def to_enrolment_id_dto(schema: EnrolmentIdSchema) -> EnrolmentIdDTO:
    return EnrolmentIdDTO(enrolment_id=schema.enrolment_id)

