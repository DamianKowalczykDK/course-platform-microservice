from datetime import datetime, timedelta, timezone
from webapp.database.models.user import User, GenderType
from webapp.database.repositories.user import UserRepository
from webapp.services.users.dtos import (
    CreateUserDTO,
    ReadUserDTO,
    LoginUserDTO,
    ResetPasswordDTO,
    ForgotPasswordDTO,
    EnableMfaDTO,
    MfaSetupDTO,
    DisableMfaDTO,
    GetMfaQrCodeDTO,
    UserIdDTO,
    IdentifierDTO,
    ResendActivationCodeDTO,
    DeleteUserByIdentifierDTO,
    DeleteUserByIdDTO
)
from webapp.services.exceptions import ConflictException, NotFoundException, ValidationException
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.services.email_service import EmailService
from flask import current_app
import uuid
import io
import base64
import pyotp
import qrcode

class UserService:
    """
    Service class for user-related operations.

    Handles creating users, activation, authentication, password reset,
    MFA management, and deletion of users. Interacts with UserRepository
    and EmailService for persistence and notifications.

    Attributes:
        user_repository (UserRepository): Repository for User entities.
        email_service (EmailService): Service for sending emails.
    """

    def __init__(self, user_repository: UserRepository, email_service: EmailService) -> None:
        """
        Initializes the UserService with the provided repository and email service.

        Args:
            user_repository (UserRepository): Repository for User entities.
            email_service (EmailService): Service for sending emails.
        """
        self.user_repository = user_repository
        self.email_service = email_service

    def create_user(self, dto: CreateUserDTO ) -> ReadUserDTO:
        """
        Creates a new user with the given details and sends an activation email.

        Args:
            dto (CreateUserDTO): DTO containing user creation details.

        Returns:
            ReadUserDTO: DTO representing the newly created user.

        Raises:
            ConflictException: If email or username already exists.
        """
        if self.user_repository.get_by_email(dto.email):
            raise ConflictException("Email already exists")

        if self.user_repository.get_by_username(dto.username):
            raise ConflictException("Username already exists")

        password_hash= generate_password_hash(dto.password)

        activation_code = str(uuid.uuid4())
        user = User(
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            gender=dto.gender,
            role=dto.role,
            password_hash=password_hash,
            activation_code=activation_code,
        )

        self.user_repository.create_user(user)

        self._send_email_with_activation_code(
            subject="Your activation code",
            to=user.email,
            username=user.username,
            activation_code=activation_code,
        )

        return self._to_read_dto(user)

    def activate_user(self, activation_code: str) -> ReadUserDTO:
        """
        Activates a user account using the provided activation code.

        Args:
            activation_code (str): Activation code sent to user's email.

        Returns:
            ReadUserDTO: DTO representing the activated user.

        Raises:
            NotFoundException: If activation code is invalid.
            ValueError: If activation code has expired.
        """
        user = self.user_repository.get_by_activation_code(activation_code)
        if not user:
            raise NotFoundException("Invalid activation code")

        expiration_minutes = current_app.config["USER_ACTIVATION_EXPIRATION_MINUTES"]

        now_utc = datetime.now(timezone.utc)
        created_at = user.activation_created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        if created_at + timedelta(minutes=expiration_minutes) < now_utc:
            raise ValueError("Activation code expired")

        user.activate()
        return self._to_read_dto(self.user_repository.save(user))

    def resend_activation_code(self, dto: ResendActivationCodeDTO) -> ReadUserDTO:
        """
        Resends a new activation code to a user who is not yet activated.

        Args:
            dto (ResendActivationCodeDTO): DTO containing username or email.

        Returns:
            ReadUserDTO: DTO representing the user with the new activation code.

        Raises:
            NotFoundException: If user does not exist.
            ValidationException: If user is already activated.
        """
        user = self.user_repository.get_by_username_or_email(dto.identifier)
        if not user:
            raise NotFoundException("Invalid username or email")
        if user.is_active:
            raise ValidationException("User already activated")

        user.update_activation_code()
        self.user_repository.save(user)

        self._send_email_with_activation_code(
            subject="Your new activation code",
            to=user.email,
            username=user.username,
            activation_code=user.activation_code,
        )

        return self._to_read_dto(user)

    def get_by_id(self, dto: UserIdDTO) -> ReadUserDTO:
        """
        Retrieves a user by ID.

        Args:
            dto (UserIdDTO): DTO containing user ID.

        Returns:
            ReadUserDTO: DTO representing the found user.

        Raises:
            NotFoundException: If user does not exist.
        """
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise NotFoundException("Active user not found")
        return self._to_read_dto(user)

    def get_by_username_or_email(self, dto: IdentifierDTO) -> ReadUserDTO:
        """
        Retrieves an active user by username or email.

        Args:
            dto (IdentifierDTO): DTO containing username or email.

        Returns:
            ReadUserDTO: DTO representing the found user.

        Raises:
            NotFoundException: If active user does not exist.
        """
        user = self.user_repository.get_active_by_username_or_email(dto.identifier)
        if not user:
            raise NotFoundException("Active user not found")

        return self._to_read_dto(user)

    def verify_credentials(self, dto: LoginUserDTO) -> ReadUserDTO:
        """
        Verifies login credentials of a user.

        Args:
            dto (LoginUserDTO): DTO containing identifier and password.

        Returns:
            ReadUserDTO: DTO representing the authenticated user.

        Raises:
            NotFoundException: If user not found.
            ValidationException: If password is invalid.
        """
        user = self.user_repository.get_active_by_username_or_email(dto.identifier)
        if not user:
            raise ValidationException("Invalid credentials")

        if not check_password_hash(user.password_hash, dto.password):
            raise ValidationException("Invalid credentials")
        return self._to_read_dto(user)

    def forgot_password(self, dto: ForgotPasswordDTO) -> None:
        """
        Initiates the password reset process for a user.

        Generates a reset token, saves it, and sends an email with reset link.

        Args:
            dto (ForgotPasswordDTO): DTO containing username or email.
        """
        user = self.user_repository.get_active_by_username_or_email(dto.identifier)
        if not user:
            return

        user.set_reset_password_token(expires_minutes=current_app.config["RESET_PASSWORD_EXPIRATION_MINUTES"])
        self.user_repository.save(user)

        resset_link = f'{current_app.config["FRONTEND_URL"]}/reset-password?token={user.reset_password_token}'

        html = f"<html><body>Reset password link: {resset_link}</body></html>"

        self.email_service.send_email(
            to=user.email,
            subject="Reset password",
            html=html,
        )

    def reset_password(self, dto: ResetPasswordDTO) -> None:
        """
        Resets the user's password using a valid reset token.

        Args:
            dto (ResetPasswordDTO): DTO containing token and new password.

        Raises:
            NotFoundException: If token is invalid or expired.
        """
        user = self.user_repository.get_by_reset_password_token(dto.token)
        if not user or not user.is_token_rest_password_valid(dto.token):
            raise NotFoundException("Invalid or expired token")

        user.reset_password(dto.new_password)
        self.user_repository.save(user)

    def enable_mfa(self, dto: EnableMfaDTO) -> MfaSetupDTO:
        """
        Enables MFA (multi-factor authentication) for a user and returns setup info.

        Args:
            dto (EnableMfaDTO): DTO containing user ID.

        Returns:
            MfaSetupDTO: DTO containing provisioning URI and QR code.

        Raises:
            NotFoundException: If user does not exist.
        """
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise NotFoundException("User not found")

        secret = pyotp.random_base32()
        user.enable_mfa_secret(secret=secret)
        self.user_repository.save(user)

        return self._generate_mfa_setup(user)

    def disable_mfa(self, dto: DisableMfaDTO) -> ReadUserDTO:
        """
        Disables MFA for a user.

        Args:
            dto (DisableMfaDTO): DTO containing user ID.

        Returns:
            ReadUserDTO: DTO representing the user after MFA is disabled.

        Raises:
            NotFoundException: If user not found.
            ValidationException: If MFA is not enabled.
        """
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise NotFoundException("User not found")

        if not user.has_mfa_secret():
            raise ValidationException("MFA is not enabled for this user")

        user.disable_mfa_secret()
        self.user_repository.save(user)

        return self._to_read_dto(user)

    def get_mfa_qrcode(self, dto: GetMfaQrCodeDTO) -> MfaSetupDTO:
        """
        Retrieves MFA QR code and provisioning URI for an existing MFA-enabled user.

        Args:
            dto (GetMfaQrCodeDTO): DTO containing user ID.

        Returns:
            MfaSetupDTO: DTO containing provisioning URI and QR code.

        Raises:
            NotFoundException: If user not found.
            ValidationException: If MFA is not enabled.
        """
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise NotFoundException("User not found")
        if not user.has_mfa_secret():
            raise ValidationException("MFA is not enabled for this user")

        return self._generate_mfa_setup(user)

    def delete_by_id(self, dto: DeleteUserByIdDTO) -> None:
        """
        Deletes a user by ID.

        Args:
            dto (DeleteUserByIdDTO): DTO containing user ID.

        Raises:
            NotFoundException: If user not found.
        """
        user_deleted = self.user_repository.delete_user_by_id(dto.user_id)
        if not user_deleted:
            raise NotFoundException("User not found")

    def delete_by_identifier(self, dto: DeleteUserByIdentifierDTO) -> None:
        """
        Deletes a user by username or email.

        Args:
            dto (DeleteUserByIdentifierDTO): DTO containing username or email.

        Raises:
            NotFoundException: If user not found.
        """
        user_deleted = self.user_repository.delete_user_by_identifier(dto.identifier)
        if not user_deleted:
            raise NotFoundException("User not found")

    def _generate_mfa_setup(self, user: User) -> MfaSetupDTO:
        """
        Generates MFA setup information including provisioning URI and QR code.

        Args:
            user (User): User object with MFA secret enabled.

        Returns:
            MfaSetupDTO: DTO containing provisioning URI and QR code in Base64.
        """
        totp = pyotp.TOTP(user.mfa_secret) #type: ignore

        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="Course Management System",
        )

        qr = qrcode.QRCode(box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_code_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        return MfaSetupDTO(
            user_id=str(user.id),
            provisioning_uri=provisioning_uri,
            qr_code_base64=qr_code_base64,
        )

    def _to_read_dto(self, user: User) -> ReadUserDTO:
        """
        Converts a User model to ReadUserDTO.

        Args:
            user (User): User model instance.

        Returns:
            ReadUserDTO: Corresponding DTO with user data.
        """
        return ReadUserDTO(
            id=str(user.id),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=GenderType(user.gender),
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )

    def _send_email_with_activation_code(
            self,
            to: str,
            subject: str,
            username: str,
            activation_code: str,
    ) -> None:
        """
        Sends an email containing an activation code to the user.

        Args:
            to (str): Recipient email address.
            subject (str): Email subject.
            username (str): User's username.
            activation_code (str): Activation code to send.
        """
        html = f'''
                    <p>Hello {username}!</p>
                    <p>Activation code: {activation_code}</p>
                '''
        self.email_service.send_email(to=to, subject=subject, html=html)