from flask import current_app
from webapp.services.enrolments.dtos import EnrolmentDTO, CreateEnrolmentDTO, EnrolmentIdDTO, EnrolmentByUserDTO, \
    DeleteEnrolmentDTO
from webapp.services.exceptions import raise_for_status
import httpx

class EnrolmentService:
    def __init__(self) -> None:
        self.enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        self.http_timeout = current_app.config["HTTP_TIMEOUT"]

    def create_enrolment_for_user(self, dto: CreateEnrolmentDTO) -> EnrolmentDTO:
        response = httpx.post(f"{self.enrolment_url}/", json=dto.__dict__, timeout=self.http_timeout)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def set_paid(self, dto: EnrolmentIdDTO) -> EnrolmentDTO:
        response = httpx.patch(f"{self.enrolment_url}/paid", json=dto.__dict__, timeout=self.http_timeout)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def expired_courses(self) -> list[EnrolmentDTO]:
        response = httpx.patch(f"{self.enrolment_url}/expired", timeout=self.http_timeout)
        raise_for_status(response)
        data = response.json()["enrolments"]
        return [EnrolmentDTO(**e) for e in data]

    def get_by_id(self, dto: EnrolmentIdDTO) -> EnrolmentDTO:
        response = httpx.get(f"{self.enrolment_url}/{dto.enrolment_id}", timeout=self.http_timeout)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def get_by_id_and_user(self, dto: EnrolmentByUserDTO) -> EnrolmentDTO:
        response = httpx.get(f"{self.enrolment_url}/{dto.enrolment_id}/details",
                             params={"user_id": dto.user_id}, timeout=self.http_timeout)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def get_active(self) -> list[EnrolmentDTO]:
        response = httpx.get(f"{self.enrolment_url}/active", timeout=self.http_timeout)
        raise_for_status(response)
        data = response.json()["enrolments"]
        return [EnrolmentDTO(**e) for e in data]

    def delete_by_id(self, dto: DeleteEnrolmentDTO) -> None:
        response = httpx.delete(f"{self.enrolment_url}/{dto.enrolment_id}", timeout=self.http_timeout)
        raise_for_status(response)
