from flask import current_app
import httpx
from webapp.services.courses.dtos import CreateCourseDTO, CourseDTO, CourseIdDTO, CourseNameDTO, UpdateCourseDTO
from webapp.services.exceptions import raise_for_status


class CourseService:
    def __init__(self) -> None:
        self.course_url = current_app.config["COURSE_SERVICE_URL"]
        self.http_timeout = current_app.config["HTTP_TIMEOUT"]

    def create_course(self, dto: CreateCourseDTO) -> CourseDTO:
        response = httpx.post(f"{self.course_url}/", json=dto.__dict__, timeout=self.http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())


    def get_by_id(self, dto: CourseIdDTO) -> CourseDTO:
        response = httpx.get(f"{self.course_url}/{dto.course_id}", timeout=self.http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def get_by_name(self, dto: CourseNameDTO) -> CourseDTO:
        response = httpx.get(f"{self.course_url}/", params={"name": dto.name}, timeout=self.http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def update_course(self, dto: UpdateCourseDTO) -> CourseDTO:
        response = httpx.patch(f"{self.course_url}/{dto.id}", json=dto.__dict__, timeout=self.http_timeout)
        raise_for_status(response)
        return CourseDTO(**response.json())

    def delete_by_id(self, dto: CourseIdDTO) -> None:
        response = httpx.delete(f"{self.course_url}/{dto.course_id}", timeout=self.http_timeout)
        raise_for_status(response)
       

