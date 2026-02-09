from webapp.services.courses.dtos import CreateCourseDTO, ReadCourseDTO, CourseIdDTO, CourseNameDTO, UpdateCourseDTO
from webapp.services.exceptions import ConflictException, NotFoundException
from webapp.services.courses.mappers import to_read_dto
from webapp.database.repositories.courses import CourseRepository
from webapp.database.models.courses import Course


class CourseService:
    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    def create_course(self, dto: CreateCourseDTO) -> ReadCourseDTO:
        if self.course_repository.get_by_name(dto.name):
            raise ConflictException("Course already exists")

        course = Course(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            max_participants=dto.max_participants,
            start_date=dto.start_date,
            end_date=dto.end_date
        )
        self.course_repository.add_and_commit(course)

        return to_read_dto(course)

    def get_by_id(self, dto: CourseIdDTO) -> ReadCourseDTO:
        course = self.course_repository.get_by_id(dto.course_id)
        if not course:
            raise NotFoundException("Course not found")

        return to_read_dto(course)

    def get_by_name(self, dto: CourseNameDTO) -> ReadCourseDTO:
        course = self.course_repository.get_by_name(dto.name)
        if not course:
            raise NotFoundException("Course not found")

        return to_read_dto(course)

    def update_course(self, dto: UpdateCourseDTO) -> ReadCourseDTO:
        course = self.course_repository.get_by_id(dto.id)
        if not course:
            raise NotFoundException("Course not found")

        course.update(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            max_participants=dto.max_participants,
            start_date=dto.start_date,
            end_date=dto.end_date
        )
        self.course_repository.add_and_commit(course)
        return to_read_dto(course)

    def delete_by_id(self, dto: CourseIdDTO) -> None:
        course = self.course_repository.get_by_id(dto.course_id)
        if not course:
            raise NotFoundException("Course not found")

        self.course_repository.delete_and_commit(course)






