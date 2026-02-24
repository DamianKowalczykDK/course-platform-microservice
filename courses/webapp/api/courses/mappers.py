from webapp.api.courses.schemas import (
    CreateCourseSchema,
    CourseResponseSchema,
    CourseIdSchema,
    CourseNameSchema,
    UpdateCourseSchema
)
from webapp.services.courses.dtos import (
    CreateCourseDTO,
    ReadCourseDTO,
    CourseIdDTO,
    CourseNameDTO,
    UpdateCourseDTO
)


def to_dto_create(schema: CreateCourseSchema) -> CreateCourseDTO:
    """
    Convert a CreateCourseSchema instance to a CreateCourseDTO.

    Args:
        schema (CreateCourseSchema): Schema with course creation data.

    Returns:
        CreateCourseDTO: DTO representing the course creation data.
    """
    return CreateCourseDTO(
        name=schema.name,
        description=schema.description,
        price=schema.price,
        max_participants=schema.max_participants,
        start_date=schema.start_date,
        end_date=schema.end_date,
    )


def to_schema_course(dto: ReadCourseDTO) -> CourseResponseSchema:
    """
    Convert a ReadCourseDTO instance to a CourseResponseSchema.

    Args:
        dto (ReadCourseDTO): DTO containing course data.

    Returns:
        CourseResponseSchema: Schema suitable for API responses.
    """
    return CourseResponseSchema(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        price=dto.price,
        max_participants=dto.max_participants,
        start_date=dto.start_date,
        end_date=dto.end_date
    )


def to_dto_course_id(schema: CourseIdSchema) -> CourseIdDTO:
    """
    Convert a CourseIdSchema instance to a CourseIdDTO.

    Args:
        schema (CourseIdSchema): Schema containing course ID.

    Returns:
        CourseIdDTO: DTO representing the course ID.
    """
    return CourseIdDTO(course_id=schema.course_id)


def to_dto_course_name(schema: CourseNameSchema) -> CourseNameDTO:
    """
    Convert a CourseNameSchema instance to a CourseNameDTO.

    Args:
        schema (CourseNameSchema): Schema containing course name.

    Returns:
        CourseNameDTO: DTO representing the course name.
    """
    return CourseNameDTO(name=schema.name)


def to_dto_update_course(course_id: int, schema: UpdateCourseSchema) -> UpdateCourseDTO:
    """
    Convert an UpdateCourseSchema instance to an UpdateCourseDTO.

    Args:
        course_id (int): The ID of the course to update.
        schema (UpdateCourseSchema): Schema containing update data.

    Returns:
        UpdateCourseDTO: DTO representing the updated course data.
    """
    return UpdateCourseDTO(
        course_id,
        name=schema.name,
        description=schema.description,
        price=schema.price,
        max_participants=schema.max_participants,
        start_date=schema.start_date,
        end_date=schema.end_date,
    )