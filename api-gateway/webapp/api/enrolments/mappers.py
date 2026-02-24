from webapp.services.enrolments.dtos import (
    CreateEnrolmentDTO,
    EnrolmentDTO,
    EnrolmentIdDTO,
    EnrolmentByUserDTO,
    DeleteEnrolmentDTO
)
from webapp.api.enrolments.schemas import (
    CreateEnrolmentSchema,
    EnrolmentResponseSchema,
    EnrolmentIdSchema,
    EnrolmentByUserSchema,
    DeleteEnrolmentSchema,
    EnrolmentsListResponseSchema
)


def to_create_enrolment_dto(schema: CreateEnrolmentSchema, user_id: str) -> CreateEnrolmentDTO:
    """
    Converts CreateEnrolmentSchema to CreateEnrolmentDTO for service layer.

    Args:
        schema (CreateEnrolmentSchema): The validated schema from API request.
        user_id (str): The ID of the user creating the enrolment.

    Returns:
        CreateEnrolmentDTO: DTO ready for the EnrolmentService.
    """
    return CreateEnrolmentDTO(user_id=user_id, course_id=schema.course_id)


def to_enrolment_response_schema(dto: EnrolmentDTO) -> EnrolmentResponseSchema:
    """
    Converts EnrolmentDTO to EnrolmentResponseSchema for API response.

    Args:
        dto (EnrolmentDTO): The DTO returned by the service layer.

    Returns:
        EnrolmentResponseSchema: Schema ready to be returned in the API response.
    """
    return EnrolmentResponseSchema(
        id=dto.id,
        user_id=dto.user_id,
        course_id=dto.course_id,
        status=dto.status,
        payment_status=dto.payment_status,
        invoice_url=dto.invoice_url
    )


def to_enrolments_list_response_schema(dtos: list[EnrolmentDTO]) -> EnrolmentsListResponseSchema:
    """
    Converts a list of EnrolmentDTOs to EnrolmentsListResponseSchema.

    Args:
        dtos (list[EnrolmentDTO]): List of DTOs returned by the service.

    Returns:
        EnrolmentsListResponseSchema: Schema containing a list of enrolment schemas.
    """
    return EnrolmentsListResponseSchema(enrolments=[to_enrolment_response_schema(dto) for dto in dtos])


def to_enrolment_id_dto(schema: EnrolmentIdSchema) -> EnrolmentIdDTO:
    """
    Converts EnrolmentIdSchema to EnrolmentIdDTO.

    Args:
        schema (EnrolmentIdSchema): Schema containing enrolment ID from API request.

    Returns:
        EnrolmentIdDTO: DTO for service layer usage.
    """
    return EnrolmentIdDTO(enrolment_id=schema.enrolment_id)


def to_enrolment_by_user_dto(schema: EnrolmentByUserSchema, user_id: str) -> EnrolmentByUserDTO:
    """
    Converts EnrolmentByUserSchema to EnrolmentByUserDTO, including user ID.

    Args:
        schema (EnrolmentByUserSchema): Schema containing enrolment ID from API request.
        user_id (str): ID of the requesting user.

    Returns:
        EnrolmentByUserDTO: DTO ready for service layer retrieval.
    """
    return EnrolmentByUserDTO(enrolment_id=schema.enrolment_id, user_id=user_id)


def to_delete_enrolment_dto(schema: DeleteEnrolmentSchema) -> DeleteEnrolmentDTO:
    """
    Converts DeleteEnrolmentSchema to DeleteEnrolmentDTO for service deletion.

    Args:
        schema (DeleteEnrolmentSchema): Schema containing enrolment ID from API request.

    Returns:
        DeleteEnrolmentDTO: DTO for deletion in the service layer.
    """
    return DeleteEnrolmentDTO(enrolment_id=schema.enrolment_id)