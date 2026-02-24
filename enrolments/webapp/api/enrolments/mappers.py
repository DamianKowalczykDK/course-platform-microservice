from webapp.api.enrolments.schemas import (
    CreateEnrolmentSchema,
    EnrolmentResponseSchema,
    EnrolmentIdSchema,
    EnrolmentByUserSchema,
    DeleteEnrolmentSchema,
    EnrolmentsListResponseSchema
)
from webapp.services.enrolments.dtos import (
    CreateEnrolmentDTO,
    ReadEnrolmentDTO,
    EnrolmentIdDTO,
    EnrolmentByUserDTO,
    DeleteEnrolmentDTO
)


def to_create_enrolment_dto(schema: CreateEnrolmentSchema) -> CreateEnrolmentDTO:
    """
    Convert a CreateEnrolmentSchema into a CreateEnrolmentDTO.

    Args:
        schema (CreateEnrolmentSchema): Input schema from the API request.

    Returns:
        CreateEnrolmentDTO: Data transfer object for service layer.
    """
    return CreateEnrolmentDTO(
        user_id=schema.user_id,
        course_id=schema.course_id,
    )


def to_enrolment_response_schema(dto: ReadEnrolmentDTO) -> EnrolmentResponseSchema:
    """
    Convert a ReadEnrolmentDTO into an EnrolmentResponseSchema for API response.

    Args:
        dto (ReadEnrolmentDTO): Service layer DTO.

    Returns:
        EnrolmentResponseSchema: Schema to return in API response.
    """
    return EnrolmentResponseSchema(
        id=dto.id,
        course_id=dto.course_id,
        user_id=dto.user_id,
        status=dto.status,
        payment_status=dto.payment_status,
        invoice_url=dto.invoice_url
    )


def to_enrolments_list_response_schema(dtos: list[ReadEnrolmentDTO]) -> EnrolmentsListResponseSchema:
    """
    Convert a list of ReadEnrolmentDTOs into an EnrolmentsListResponseSchema.

    Args:
        dtos (list[ReadEnrolmentDTO]): List of service layer DTOs.

    Returns:
        EnrolmentsListResponseSchema: Schema containing list of enrolments.
    """
    return EnrolmentsListResponseSchema(enrolments=[to_enrolment_response_schema(dto) for dto in dtos])


def to_enrolment_id_dto(schema: EnrolmentIdSchema) -> EnrolmentIdDTO:
    """
    Convert an EnrolmentIdSchema into an EnrolmentIdDTO.

    Args:
        schema (EnrolmentIdSchema): Input schema from API request.

    Returns:
        EnrolmentIdDTO: DTO to identify a single enrolment.
    """
    return EnrolmentIdDTO(enrolment_id=schema.enrolment_id)


def to_enrolment_by_user_dto(schema: EnrolmentByUserSchema) -> EnrolmentByUserDTO:
    """
    Convert an EnrolmentByUserSchema into an EnrolmentByUserDTO.

    Args:
        schema (EnrolmentByUserSchema): Input schema containing enrolment ID and user ID.

    Returns:
        EnrolmentByUserDTO: DTO for service layer operations.
    """
    return EnrolmentByUserDTO(enrolment_id=schema.enrolment_id, user_id=schema.user_id)


def to_enrolment_delete_dto(schema: DeleteEnrolmentSchema) -> DeleteEnrolmentDTO:
    """
    Convert a DeleteEnrolmentSchema into a DeleteEnrolmentDTO.

    Args:
        schema (DeleteEnrolmentSchema): Input schema from API request.

    Returns:
        DeleteEnrolmentDTO: DTO for deleting an enrolment.
    """
    return DeleteEnrolmentDTO(enrolment_id=schema.enrolment_id)