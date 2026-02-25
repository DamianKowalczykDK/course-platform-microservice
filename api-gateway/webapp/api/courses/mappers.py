from webapp.api.courses.schemas import (
    CreateCourseSchema,
    CourseResponseSchema,
    CourseIdSchema,
    CourseNameSchema,
    UpdateCourseSchema,
    CoursesListResponseSchema
)
from webapp.services.courses.dtos import (
    CreateCourseDTO,
    CourseDTO,
    CourseIdDTO,
    CourseNameDTO,
    UpdateCourseDTO
)


def to_dto_create(schema: CreateCourseSchema) -> CreateCourseDTO:
    """
    Map CreateCourseSchema (from API) to CreateCourseDTO (service layer).

    Args:
        schema (CreateCourseSchema): Incoming validated schema for course creation.

    Returns:
        CreateCourseDTO: DTO used by CourseService for creating a course.
    """
    return CreateCourseDTO(
        name=schema.name,
        description=schema.description,
        price=schema.price,
        max_participants=schema.max_participants,
        start_date=schema.start_date,
        end_date=schema.end_date,
    )


def to_schema_course(dto: CourseDTO) -> CourseResponseSchema:
    """
    Map CourseDTO (service layer) to CourseResponseSchema (API response).

    Args:
        dto (CourseDTO): DTO representing course details.

    Returns:
        CourseResponseSchema: Schema ready to be returned in API response.
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

def to_schema_list_course(dtos: list[CourseDTO]) -> CoursesListResponseSchema:
    """
        Convert a list of CourseDTOs to a CoursesListResponseSchema.

        Args:
            dtos (list[CourseDTO]): List of course DTOs to convert.

        Returns:
            CoursesListResponseSchema: Schema containing the list of courses.
        """
    return CoursesListResponseSchema(courses=[to_schema_course(dto) for dto in dtos])

def to_dto_course_id(schema: CourseIdSchema) -> CourseIdDTO:
    """
    Map CourseIdSchema (API) to CourseIdDTO (service layer).

    Args:
        schema (CourseIdSchema): Schema containing course ID.

    Returns:
        CourseIdDTO: DTO for service operations requiring a course ID.
    """
    return CourseIdDTO(course_id=schema.course_id)


def to_dto_course_name(schema: CourseNameSchema) -> CourseNameDTO:
    """
    Map CourseNameSchema (API) to CourseNameDTO (service layer).

    Args:
        schema (CourseNameSchema): Schema containing course name.

    Returns:
        CourseNameDTO: DTO for service operations requiring a course name.
    """
    return CourseNameDTO(name=schema.name)


def to_dto_update_course(course_id: int, schema: UpdateCourseSchema) -> UpdateCourseDTO:
    """
    Map UpdateCourseSchema (API) to UpdateCourseDTO (service layer) with the course ID.

    Args:
        course_id (int): ID of the course to update.
        schema (UpdateCourseSchema): Schema containing updated fields.

    Returns:
        UpdateCourseDTO: DTO used by CourseService to update the course.
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