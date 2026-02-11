from flask import current_app
from webapp.services.enrolments.dtos import EnrolmentDTO, CreateEnrolmentDTO, EnrolmentIdDTO
from webapp.services.exceptions import raise_for_status
import httpx

class EnrolmentService:
    def create_enrolment_for_user(self, dto: CreateEnrolmentDTO) -> EnrolmentDTO:
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        response = httpx.post(f"{enrolment_url}/", json=dto.__dict__, timeout=5)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())
