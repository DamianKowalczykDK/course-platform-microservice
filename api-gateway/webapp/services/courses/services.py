from flask import current_app
from webapp.services.courses.dtos import (
    CreateCourseDTO,
    CourseDTO,
    CourseIdDTO,
    CourseNameDTO,
    UpdateCourseDTO
)
from webapp.services.exceptions import raise_for_status
import httpx


class CourseService:
    """Service for interacting with the Courses microservice via HTTP."""

    def create_course(self, dto: CreateCourseDTO) -> CourseDTO:
        """
        Create a new course.

        Args:
            dto (CreateCourseDTO): Data required to create a course.

        Returns:
            CourseDTO: Created course details.
        """
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.post(f"{course_url}/", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def get_by_id(self, dto: CourseIdDTO) -> CourseDTO:
        """
        Retrieve course details by course ID.

        Args:
            dto (CourseIdDTO): DTO containing the ID of the course.

        Returns:
            CourseDTO: Course details.
        """
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{course_url}/{dto.course_id}", timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def get_by_name(self, dto: CourseNameDTO) -> CourseDTO:
        """
        Retrieve course details by course name.

        Args:
            dto (CourseNameDTO): DTO containing the name of the course.

        Returns:
            CourseDTO: Course details.
        """
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{course_url}/", params={"name": dto.name}, timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def update_course(self, dto: UpdateCourseDTO) -> CourseDTO:
        """
        Update an existing course.

        Args:
            dto (UpdateCourseDTO): DTO containing course ID and fields to update.

        Returns:
            CourseDTO: Updated course details.
        """
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.patch(f"{course_url}/{dto.id}", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def delete_by_id(self, dto: CourseIdDTO) -> None:
        """
        Delete a course by its ID.

        Args:
            dto (CourseIdDTO): DTO containing the ID of the course to delete.

        Returns:
            None
        """
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.delete(f"{course_url}/{dto.course_id}", timeout=http_timeout)
        raise_for_status(response)