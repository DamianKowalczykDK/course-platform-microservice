from webapp.database.models.enrolments import Enrolment, PaymentStatus
from webapp.database.repositories.enrolments import EnrolmentRepository
from webapp.services.email_service import EmailService
from webapp.services.enrolments.dtos import (
    CreateEnrolmentDTO,
    ReadEnrolmentDTO,
    EnrolmentIdDTO,
    EnrolmentByUserDTO,
    DeleteEnrolmentDTO
)
from webapp.services.enrolments.mappers import to_read_dto
from webapp.services.exceptions import (
    ValidationException,
    NotFoundException,
    ConflictException,
    ServiceException
)
from webapp.extensions import db
from webapp.services.invoices.services import InvoiceService
from webapp.services.invoices.dtos import InvoiceDTO
from webapp.extensions import executor
from flask import current_app, copy_current_request_context
import httpx


class EnrolmentService:
    """
    Service for managing enrolments, including CRUD operations,
    payment handling, and expired enrolment processing.

    Attributes:
        repo (EnrolmentRepository): Repository for enrolment data access.
        email_service (EmailService): Service to send emails.
        invoice_service (InvoiceService): Service to generate invoices.
    """

    def __init__(
            self,
            enrolment_repository: EnrolmentRepository,
            email_service: EmailService,
            invoice_service: InvoiceService
    ) -> None:
        """Initialize the EnrolmentService with dependencies."""
        self.repo = enrolment_repository
        self.email_service = email_service
        self.invoice_service = invoice_service

    def create_enrolment_for_user(self, dto: CreateEnrolmentDTO) -> ReadEnrolmentDTO:
        """
        Create a new enrolment for a user and send confirmation email.

        Args:
            dto (CreateEnrolmentDTO): DTO containing user_id and course_id.

        Returns:
            ReadEnrolmentDTO: DTO with created enrolment details.

        Raises:
            ServiceException: If external service fails or unknown error occurs.
            ValidationException, NotFoundException, ConflictException: For domain validation errors.
        """
        try:
            user_data = self._user_data(dto.user_id)
            course_data = self._course_data(dto.course_id)

            course_id = int(course_data["id"])
            course_end_data = course_data["end_date"]
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
        """
        Mark an enrolment as paid, generate invoice, and send confirmation email.

        Args:
            dto (EnrolmentIdDTO): DTO containing enrolment ID.

        Returns:
            ReadEnrolmentDTO: DTO with updated enrolment status.

        Raises:
            NotFoundException: If enrolment does not exist.
            ConflictException: If enrolment is already paid.
        """
        enrolment = self.repo.get_by_id(dto.enrolment_id)

        if not enrolment:
            raise NotFoundException(f"Enrolment not found")
        if enrolment.payment_status == PaymentStatus.PAID:
            raise ConflictException(f"Enrolment already paid")

        user_data = self._user_data(enrolment.user_id)
        course_data = self._course_data(enrolment.course_id)
        user_email = user_data["email"]

        enrolment.payment_status = PaymentStatus.PAID

        invoice_data = InvoiceDTO(
            client_name=f"{user_data['first_name']} {user_data['last_name']}",
            client_email=user_data["email"],
            course_name=course_data["name"],
            price=int(course_data["price"]),
        )

        invoice_url = self.invoice_service.create_invoice(invoice_data)
        enrolment.invoice_url = invoice_url

        @copy_current_request_context
        def send_email() -> None:
            self._send_payment_email(user_email, invoice_url)

        executor.submit(send_email)
        db.session.commit()

        return to_read_dto(enrolment)

    def expired_courses(self) -> list[ReadEnrolmentDTO]:
        """
        Mark expired enrolments as completed and return updated list.

        Returns:
            list[ReadEnrolmentDTO]: List of DTOs for updated enrolments.
        """
        updated_enrolments = self.repo.mark_expired_enrolments_completed()
        db.session.commit()
        return [to_read_dto(e) for e in updated_enrolments]

    def get_by_id(self, dto: EnrolmentIdDTO) -> ReadEnrolmentDTO:
        """
        Get enrolment by its ID.

        Args:
            dto (EnrolmentIdDTO): DTO containing enrolment ID.

        Returns:
            ReadEnrolmentDTO: DTO for the enrolment.

        Raises:
            NotFoundException: If enrolment does not exist.
        """
        enrolment = self.repo.get_by_id(dto.enrolment_id)
        if not enrolment:
            raise NotFoundException(f"Enrolment not found")
        return to_read_dto(enrolment)

    def get_by_id_and_user(self, dto: EnrolmentByUserDTO) -> ReadEnrolmentDTO:
        """
        Get enrolment by ID and user ID.

        Args:
            dto (EnrolmentByUserDTO): DTO containing enrolment ID and user ID.

        Returns:
            ReadEnrolmentDTO: DTO for the enrolment.

        Raises:
            NotFoundException: If enrolment does not exist for given user.
        """
        enrolment = self.repo.get_by_id_and_user(enrolment_id=dto.enrolment_id, user_id=dto.user_id)
        if not enrolment:
            raise NotFoundException(f"Enrolment not found")
        return to_read_dto(enrolment)

    def get_active(self) -> list[ReadEnrolmentDTO]:
        """
        Get all active enrolments.

        Returns:
            list[ReadEnrolmentDTO]: List of active enrolments.

        Raises:
            NotFoundException: If no active enrolments exist.
        """
        enrolments = self.repo.get_active()
        
        return [to_read_dto(e) for e in enrolments]

    def delete_by_id(self, dto: DeleteEnrolmentDTO) -> None:
        """
        Delete an enrolment by its ID.

        Args:
            dto (DeleteEnrolmentDTO): DTO containing enrolment ID.

        Raises:
            NotFoundException: If enrolment does not exist.
        """
        enrolment = self.repo.get_by_id(dto.enrolment_id)
        if not enrolment:
            raise NotFoundException(f"Enrolment not found")
        self.repo.delete_and_commit(enrolment)

    def _user_data(self, user_id: str) -> dict[str, str]:
        """
        Fetch user data from the Users Service.

        Args:
            user_id (str): ID of the user.

        Returns:
            dict[str, str]: User information from the service.

        Raises:
            ValidationException: If user does not exist or inactive.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        user_resp = httpx.get(f"{users_url}/id", params={"user_id": user_id}, timeout=http_timeout)
        if user_resp.status_code != 200:
            raise ValidationException(f"User not found or inactive")
        return user_resp.json()

    def _course_data(self, course_id: int) -> dict[str, str]:
        """
        Fetch course data from the Courses Service.

        Args:
            course_id (int): ID of the course.

        Returns:
            dict[str, str]: Course information from the service.

        Raises:
            ValidationException: If course does not exist.
        """
        course_url = current_app.config["COURSE_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        course_resp = httpx.get(f"{course_url}/{course_id}", timeout=http_timeout)
        if course_resp.status_code != 200:
            raise ValidationException(f"Course {course_id} not found")
        return course_resp.json()

    def _send_payment_email(self, user_email: str, invoice_url: str) -> None:
        """
        Send payment confirmation email with invoice link.

        Args:
            user_email (str): Recipient email address.
            invoice_url (str): URL to the invoice PDF.
        """
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