from flask import current_app
from webapp.services.enrolments.dtos import EnrolmentDTO, CreateEnrolmentDTO, EnrolmentIdDTO, EnrolmentByUserDTO
from webapp.services.exceptions import raise_for_status
import httpx

class EnrolmentService:
    def create_enrolment_for_user(self, dto: CreateEnrolmentDTO) -> EnrolmentDTO:
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        response = httpx.post(f"{enrolment_url}/", json=dto.__dict__, timeout=5)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def set_paid(self, dto: EnrolmentIdDTO) -> EnrolmentDTO:
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        response = httpx.patch(f"{enrolment_url}/paid", json=dto.__dict__, timeout=5)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def expired_courses(self) -> list[EnrolmentDTO]:
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        response = httpx.patch(f"{enrolment_url}/expired", timeout=5)
        raise_for_status(response)
        return [EnrolmentDTO(**e) for e in response.json()]

    def get_by_id(self, dto: EnrolmentIdDTO) -> EnrolmentDTO:
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        response = httpx.get(f"{enrolment_url}/{dto.enrolment_id}", timeout=5)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def get_by_id_and_user(self, dto: EnrolmentByUserDTO) -> EnrolmentDTO:
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        response = httpx.get(f"{enrolment_url}/{dto.enrolment_id}/details", params={"user_id": dto.user_id}, timeout=5)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())
