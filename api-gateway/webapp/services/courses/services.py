from flask import current_app
import httpx
from webapp.services.courses.dtos import CreateCourseDTO, CourseDTO, CourseIdDTO, CourseNameDTO, UpdateCourseDTO
from webapp.services.exceptions import raise_for_status


class CourseService:

    def create_course(self, dto: CreateCourseDTO) -> CourseDTO:
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.post(f"{course_url}/", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())


    def get_by_id(self, dto: CourseIdDTO) -> CourseDTO:
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{course_url}/{dto.course_id}", timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def get_by_name(self, dto: CourseNameDTO) -> CourseDTO:
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{course_url}/", params={"name": dto.name}, timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def update_course(self, dto: UpdateCourseDTO) -> CourseDTO:
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.patch(f"{course_url}/{dto.id}", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def delete_by_id(self, dto: CourseIdDTO) -> None:
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.delete(f"{course_url}/{dto.course_id}", timeout=http_timeout)
        raise_for_status(response)
       

