from webapp.database.models.enrolments import Enrolment, PaymentStatus, Status
from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.services.email_service import EmailService
from webapp.services.enrolments.dtos import CreateEnrolmentDTO, ReadEnrolmentDTO, EnrolmentIdDTO, EnrolmentByUserDTO
from webapp.services.enrolments.mappers import to_read_dto
from webapp.services.exceptions import ValidationException, NotFoundException, ConflictException, ServiceException
from webapp.extensions import db
from webapp.services.invoices.services import InvoiceService
from webapp.services.invoices.dtos import InvoiceDTO
from datetime import datetime, timezone
from flask import current_app
import httpx


class EnrolmentService:
    def __init__(
            self,
            enrolment_repository: EnrolmentRepository,
            email_service: EmailService,
            invoice_service: InvoiceService

    ) -> None:
        self.repo = enrolment_repository
        self.email_service = email_service
        self.invoice_service = invoice_service



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
            course_end_data = course_data["end_date"]

            user_data = user_resp.json()
            user_email = user_data["email"]

            with db.session.begin():
                entity = Enrolment(
                    course_id=course_id,
                    user_id=dto.user_id,
                    course_end_date=course_end_data,
                )
                db.session.add(entity)
            html = f"""
            <html>
              <body>
                <h2>Thank you for enrolling in the course {course_data["name"]}!</h2>
                <p>Your enrolment has been successfully recorded.</p>
              </body>
            </html>
            """

            self.email_service.send_email(to=user_email, subject="Course enrolment confirmation", html=html)

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
        course_url = current_app.config["COURSE_SERVICE_URL"]

        if not enrolment:
            raise NotFoundException(f"Enrolment not found")

        if enrolment.payment_status == PaymentStatus.PAID:
            raise ConflictException(f"Enrolment already paid")

        user_resp = httpx.get(f"{users_url}/id", params={"user_id": enrolment.user_id}, timeout=5)
        if user_resp.status_code != 200:
            raise ValidationException(f"User not found or inactive")

        course_resp = httpx.get(f"{course_url}/{enrolment.course_id}", timeout=5)
        if course_resp.status_code != 200:
            raise ValidationException(f"Course {enrolment.course_id} not found")

        course_data = course_resp.json()


        user_data = user_resp.json()
        user_email = user_data["email"]


        enrolment.payment_status = PaymentStatus.PAID


        invoice_data = InvoiceDTO(
            client_name=f"{user_data["first_name"]} {user_data['last_name']}",
            client_email=user_data["email"],
            course_name=course_data["name"],
            price=course_data["price"],
        )

        invoice_url = self.invoice_service.create_invoice(invoice_data)
        enrolment.invoice_url = invoice_url

        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
            <h2>Thank you for your payment!</h2>
            <p>Your course has been successfully paid.</p>
            <p>You can download your invoice here: <a href="{invoice_url}">{invoice_url}</a></p>
            <p>We look forward to seeing you in the course!</p>
          </body>
        </html>
        """

        self.email_service.send_email(to=user_email, subject=f"Your course payment confirmation", html=html)
        db.session.commit()

        return to_read_dto(enrolment)


    def expired_courses(self) -> list[ReadEnrolmentDTO]:
        updated_enrolments = self.repo.mark_expired_enrolments_completed()

        return [to_read_dto(e) for e in updated_enrolments]


    def get_by_id(self, dto: EnrolmentIdDTO) -> ReadEnrolmentDTO:
        enrolment = self.repo.get_by_id(dto.enrolment_id)

        if not enrolment:
            raise NotFoundException(f"Enrolment not found")

        return to_read_dto(enrolment)

    def get_by_id_and_user(self, dto: EnrolmentByUserDTO) -> ReadEnrolmentDTO:
        enrolment = self.repo.get_by_id_and_user(enrolment_id=dto.enrolment_id, user_id=dto.user_id)
        if not enrolment:
            raise NotFoundException(f"Enrolment not found")
        return to_read_dto(enrolment)

    def get_active(self) -> list[ReadEnrolmentDTO]:
         enrolments = self.repo.get_active()

         if not enrolments:
            raise NotFoundException(f"Enrolments not found")
         return [to_read_dto(e) for e in enrolments]
