from webapp.api.courses.schemas import CreateCourseSchema, CourseResponseSchema, CourseIdSchema, CourseNameSchema, \
    UpdateCourseSchema
from webapp.services.courses.dtos import CreateCourseDTO, ReadCourseDTO, CourseIdDTO, CourseNameDTO, UpdateCourseDTO


def to_dto_create(schema: CreateCourseSchema) -> CreateCourseDTO:
    return CreateCourseDTO(
        name=schema.name,
        description=schema.description,
        max_participants=schema.max_participants,
        start_date=schema.start_date,
        end_date=schema.end_date,
    )

def to_schema_course(dto: ReadCourseDTO) -> CourseResponseSchema:
    return CourseResponseSchema(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        max_participants=dto.max_participants,
        start_date=dto.start_date,
        end_date=dto.end_date
    )

def to_dto_course_id(schema: CourseIdSchema) -> CourseIdDTO:
    return CourseIdDTO(course_id=schema.course_id)

def to_dto_course_name(schema: CourseNameSchema) -> CourseNameDTO:
    return CourseNameDTO(name=schema.name)

def to_dto_update_course(course_id: int, schema: UpdateCourseSchema) -> UpdateCourseDTO:
    return UpdateCourseDTO(
        course_id,
        name=schema.name,
        description=schema.description,
        max_participants=schema.max_participants,
        start_date=schema.start_date,
        end_date=schema.end_date,
    )