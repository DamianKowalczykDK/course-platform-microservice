from sqlalchemy.exc import IntegrityError
from webapp.services.courses.dtos import (
    CreateCourseDTO,
    ReadCourseDTO,
    CourseIdDTO,
    CourseNameDTO,
    UpdateCourseDTO
)
from webapp.services.exceptions import ConflictException, NotFoundException
from webapp.services.courses.mappers import to_read_dto
from webapp.database.repositories.courses import CourseRepository
from webapp.database.models.courses import Course


class CourseService:
    """
    Service layer responsible for handling business logic related to courses.

    Provides operations for creating, retrieving, updating, and deleting
    Course entities. Handles validation rules and translates repository
    results into Data Transfer Objects (DTOs).
    """

    def __init__(self, course_repository: CourseRepository):
        """
        Initialize the CourseService.

        Args:
            course_repository (CourseRepository): Repository used for
                Course persistence operations.
        """
        self.course_repository = course_repository

    def create_course(self, dto: CreateCourseDTO) -> ReadCourseDTO:
        """
        Create a new course.

        Validates that a course with the same name does not already exist.
        Persists the new course in the database and returns its DTO representation.

        Args:
            dto (CreateCourseDTO): Data required to create a new course.

        Raises:
            ConflictException: If a course with the same name already exists.

        Returns:
            ReadCourseDTO: DTO representation of the created course.
        """
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
        try:
            self.course_repository.add_and_commit(course)
        except IntegrityError:
            self.course_repository.rollback()

        return to_read_dto(course)

    def get_by_id(self, dto: CourseIdDTO) -> ReadCourseDTO:
        """
        Retrieve a course by its identifier.

        Args:
            dto (CourseIdDTO): DTO containing the course ID.

        Raises:
            NotFoundException: If the course does not exist.

        Returns:
            ReadCourseDTO: DTO representation of the found course.
        """
        course = self.course_repository.get_by_id(dto.course_id)
        if not course:
            raise NotFoundException("Course not found")

        return to_read_dto(course)

    def get_by_name(self, dto: CourseNameDTO) -> ReadCourseDTO:
        """
        Retrieve a course by its name.

        Args:
            dto (CourseNameDTO): DTO containing the course name.

        Raises:
            NotFoundException: If the course does not exist.

        Returns:
            ReadCourseDTO: DTO representation of the found course.
        """
        course = self.course_repository.get_by_name(dto.name)
        if not course:
            raise NotFoundException("Course not found")

        return to_read_dto(course)

    def update_course(self, dto: UpdateCourseDTO) -> ReadCourseDTO:
        """
        Update an existing course.

        Only non-None fields from the DTO are applied to the course entity.
        The updated course is persisted and returned as a DTO.

        Args:
            dto (UpdateCourseDTO): DTO containing updated course data.

        Raises:
            NotFoundException: If the course does not exist.

        Returns:
            ReadCourseDTO: DTO representation of the updated course.
        """
        course = self.course_repository.get_by_id(dto.id)
        if not course:
            raise NotFoundException("Course not found")

        course.update(update_data={
            "name": dto.name,
            "description": dto.description,
            "price": dto.price,
            "max_participants": dto.max_participants,
            "start_date": dto.start_date,
            "end_date": dto.end_date

        })
        self.course_repository.add_and_commit(course)
        return to_read_dto(course)

    def delete_by_id(self, dto: CourseIdDTO) -> None:
        """
        Delete a course by its identifier.

        Args:
            dto (CourseIdDTO): DTO containing the course ID.

        Raises:
            NotFoundException: If the course does not exist.
        """
        course = self.course_repository.get_by_id(dto.course_id)
        if not course:
            raise NotFoundException("Course not found")

        self.course_repository.delete_and_commit(course)