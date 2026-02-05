from webapp.database.models.enrolments import Enrolment, PaymentStatus, Status
from webapp.database.repositories.enrolments import EnrolmentRepository
from flask import current_app
from webapp.services.enrolments.dtos import CreateEnrolmentDTO, ReadEnrolmentDTO
from webapp.services.enrolments.mappers import to_read_dto
from webapp.services.exceptions import ApiException, ValidationException, NotFoundException, ConflictException, ServerException
from webapp.extensions import db
import httpx

class EnrolmentService:
    def __init__(self, enrolment_repository: EnrolmentRepository) -> None:
        self.repo = enrolment_repository

    def create_course_for_user(self, dto: CreateEnrolmentDTO) -> ReadEnrolmentDTO:
        course_url = current_app.config["COURSE_SERVICE_URL"]
        users_url = current_app.config["USERS_SERVICE_URL"]

        try:

            user_resp = httpx.get(f"{users_url}/id", params={"user_id": dto.user_id}, timeout=5)
            if user_resp.status_code != 200:
                raise ValidationException(f"User {dto.user_id} not found or inactive")

            course_resp = httpx.get(f"{course_url}/{dto.course_id}", timeout=5)
            if course_resp.status_code != 200:
                raise ValidationException(f"Course {dto.course_id} not found")

            course_data = course_resp.json()
            course_id = int(course_data["id"])

            with db.session.begin():
                entity = Enrolment(
                    course_id=course_id,
                    user_id=dto.user_id,
                )
                db.session.add(entity)


            return to_read_dto(entity)


        except httpx.RequestError as e:
            raise ServerException(f"HTTP Request Error: {e}")
        except Exception as e:
            raise ServerException(f"Unknown Server Error: {e}")
