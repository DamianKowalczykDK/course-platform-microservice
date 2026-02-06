from webapp.database.models.enrolments import Enrolment, PaymentStatus, Status
from webapp.database.repositories.enrolments import EnrolmentRepository
from flask import current_app

from webapp.services.email_service import EmailService
from webapp.services.enrolments.dtos import CreateEnrolmentDTO, ReadEnrolmentDTO, EnrolmentIdDTO
from webapp.services.enrolments.mappers import to_read_dto
from webapp.services.exceptions import ValidationException, NotFoundException, ConflictException, ServiceException
from webapp.extensions import db
import httpx

class EnrolmentService:
    def __init__(self, enrolment_repository: EnrolmentRepository, email_service: EmailService) -> None:
        self.repo = enrolment_repository
        self.email_service = email_service


    def create_enrolment_for_user(self, dto: CreateEnrolmentDTO) -> ReadEnrolmentDTO:
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

            user_data = user_resp.json()
            user_email = user_data["email"]

            with db.session.begin():
                entity = Enrolment(
                    course_id=course_id,
                    user_id=dto.user_id,
                )
                db.session.add(entity)
            html = f"<html><body>Your invoice link: </body></html>"

            self.email_service.send_email(to=user_email, subject="Thank you for enrolment", html=html)


            return to_read_dto(entity)


        except httpx.RequestError as e:
            raise ServiceException(f"HTTP Request Error: {e}")
        except (ValidationException, NotFoundException, ConflictException):
            raise
        except Exception as e:
            raise ServiceException(f"Unknown Server Error: {e}")

    def set_paid(self, dto: EnrolmentIdDTO) -> ReadEnrolmentDTO:
        enrolment = self.repo.get_by_id(dto.enrolment_id)
        users_url = current_app.config["USERS_SERVICE_URL"]

        if not enrolment:
            raise NotFoundException(f"Enrolment not found")

        if enrolment.payment_status == PaymentStatus.PAID:
            raise ConflictException(f"Enrolment already paid")

        user_resp = httpx.get(f"{users_url}/id", params={"user_id": enrolment.user_id}, timeout=5)
        if user_resp.status_code != 200:
            raise ValidationException(f"User not found or inactive")

        user_data = user_resp.json()
        user_email = user_data["email"]


        enrolment.payment_status = PaymentStatus.PAID
        db.session.commit()

        html = f"<html><body>Your course has been paid, Thank you.</body></html>"
        self.email_service.send_email(to=user_email, subject=f"Thank you for paying", html=html)

        return to_read_dto(enrolment)

    def get_by_id(self, dto: EnrolmentIdDTO) -> ReadEnrolmentDTO:
        enrolment = self.repo.get_by_id(dto.enrolment_id)

        if not enrolment:
            raise NotFoundException(f"Enrolment not found")

        return to_read_dto(enrolment)