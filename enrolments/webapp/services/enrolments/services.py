from webapp.database.models.enrolments import Enrolment, PaymentStatus, Status
from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.services.email_service import EmailService
from webapp.services.enrolments.dtos import CreateEnrolmentDTO, ReadEnrolmentDTO, EnrolmentIdDTO
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
        db.session.commit()

        invoice_data = InvoiceDTO(
            client_name=f"{user_data["first_name"]} {user_data['last_name']}",
            client_email=user_data["email"],
            course_name=course_data["name"],
            price=course_data["price"],
        )

        invoice_url = self.invoice_service.create_invoice(invoice_data)
        enrolment.invoice_url = invoice_url

        html = f"<html><body>Your course has been paid, your invoice:\n {invoice_url}</body></html>"
        self.email_service.send_email(to=user_email, subject=f"Thank you for paying", html=html)

        return to_read_dto(enrolment)


    def expired_courses(self) -> list[ReadEnrolmentDTO]:
        course_url = current_app.config["COURSE_SERVICE_URL"]
        active_enrolments = self.repo.get_active()

        enrolments_completed = []

        for enrolment in active_enrolments:
            course_resp = httpx.get(f"{course_url}/{enrolment.course_id}", timeout=5)
            if course_resp.status_code != 200:
                continue

            course_data = course_resp.json()
            course_end_date = course_data["end_date"]
            end_date = datetime.fromisoformat(course_end_date).replace(tzinfo=timezone.utc)

            now_utc = datetime.now(timezone.utc)
            if end_date < now_utc:
                enrolment.status = Status.COMPLETED
                enrolments_completed.append(enrolment)
                db.session.commit()

        return [to_read_dto(e) for e in enrolments_completed]


    def get_by_id(self, dto: EnrolmentIdDTO) -> ReadEnrolmentDTO:
        enrolment = self.repo.get_by_id(dto.enrolment_id)

        if not enrolment:
            raise NotFoundException(f"Enrolment not found")

        return to_read_dto(enrolment)

    def get_active(self) -> list[ReadEnrolmentDTO]:
         enrolments = self.repo.get_active()

         if not enrolments:
            raise NotFoundException(f"Enrolments not found")
         return [to_read_dto(e) for e in enrolments]
