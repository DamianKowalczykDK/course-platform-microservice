from flask import current_app
from webapp.services.enrolments.dtos import (
    EnrolmentDTO,
    CreateEnrolmentDTO,
    EnrolmentIdDTO,
    EnrolmentByUserDTO,
    DeleteEnrolmentDTO
)
from webapp.services.exceptions import raise_for_status
import httpx

class EnrolmentService:
    """
    Service for interacting with the Enrolments microservice via HTTP.

    Provides methods for creating enrolments, marking them as paid,
    fetching by ID or user, listing active enrolments, and deleting enrolments.
    """

    def create_enrolment_for_user(self, dto: CreateEnrolmentDTO) -> EnrolmentDTO:
        """
        Create a new enrolment for a given user and course.

        Args:
            dto (CreateEnrolmentDTO): DTO containing user_id and course_id.

        Returns:
            EnrolmentDTO: The created enrolment.
        """
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.post(f"{enrolment_url}/", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def set_paid(self, dto: EnrolmentIdDTO) -> EnrolmentDTO:
        """
        Mark an enrolment as paid.

        Args:
            dto (EnrolmentIdDTO): DTO containing the enrolment ID.

        Returns:
            EnrolmentDTO: The updated enrolment with payment_status set to PAID.
        """
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.patch(f"{enrolment_url}/paid", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def expired_courses(self) -> list[EnrolmentDTO]:
        """
        Mark all expired courses as completed and return affected enrolments.

        Returns:
            list[EnrolmentDTO]: List of enrolments that were updated.
        """
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.patch(f"{enrolment_url}/expired", timeout=http_timeout)
        raise_for_status(response)
        data = response.json()["enrolments"]
        return [EnrolmentDTO(**e) for e in data]

    def get_by_id(self, dto: EnrolmentIdDTO) -> EnrolmentDTO:
        """
        Fetch an enrolment by its unique ID.

        Args:
            dto (EnrolmentIdDTO): DTO containing the enrolment ID.

        Returns:
            EnrolmentDTO: The fetched enrolment.
        """
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{enrolment_url}/{dto.enrolment_id}", timeout=http_timeout)
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def get_by_id_and_user(self, dto: EnrolmentByUserDTO) -> EnrolmentDTO:
        """
        Fetch an enrolment by its ID and associated user ID.

        Args:
            dto (EnrolmentByUserDTO): DTO containing enrolment ID and user ID.

        Returns:
            EnrolmentDTO: The fetched enrolment.
        """
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(
            f"{enrolment_url}/{dto.enrolment_id}/details",
            params={"user_id": dto.user_id},
            timeout=http_timeout
        )
        raise_for_status(response)
        return EnrolmentDTO(**response.json())

    def get_active(self) -> list[EnrolmentDTO]:
        """
        Fetch all currently active enrolments.

        Returns:
            list[EnrolmentDTO]: List of active enrolments.
        """
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{enrolment_url}/active", timeout=http_timeout)
        raise_for_status(response)
        data = response.json()["enrolments"]
        return [EnrolmentDTO(**e) for e in data]

    def delete_by_id(self, dto: DeleteEnrolmentDTO) -> None:
        """
        Delete an enrolment by its ID.

        Args:
            dto (DeleteEnrolmentDTO): DTO containing the enrolment ID.
        """
        enrolment_url = current_app.config["ENROLMENT_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.delete(f"{enrolment_url}/{dto.enrolment_id}", timeout=http_timeout)
        raise_for_status(response)