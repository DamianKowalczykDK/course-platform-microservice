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
    MfaSetupDTO
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
    def __init__(self, user_repository: UserRepository, email_service: EmailService) -> None:
        self.user_repository = user_repository
        self.email_service = email_service

    def create_user(self, dto: CreateUserDTO ) -> ReadUserDTO:
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
        user = self.user_repository.get_by_activation_code(activation_code)
        if user is None:
            raise NotFoundException("Invalid activation code")

        expiration_minutes = current_app.config["USER_ACTIVATION_EXPIRATION_MINUTES"]

        now_utc = datetime.now(timezone.utc)
        created_at = user.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        if created_at + timedelta(minutes=expiration_minutes) < now_utc:
            raise ValueError("Activation code expired")

        user.activate()
        return self._to_read_dto(self.user_repository.save(user))

    def resend_activation_code(self, identifier: str) -> ReadUserDTO:
        user = self.user_repository.get_by_username_or_email(identifier)
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

    def get_by_username_or_email(self, identifier: str) -> ReadUserDTO:
        user = self.user_repository.get_active_by_username_or_email(identifier)
        if user is None:
            raise NotFoundException("Active user not found")

        return self._to_read_dto(user)

    def verify_credentials(self, dto: LoginUserDTO) -> ReadUserDTO:
        user = self.user_repository.get_active_by_username_or_email(dto.identifier)
        if user is None:
            raise NotFoundException("Invalid credentials -1")

        if not check_password_hash(user.password_hash, dto.password):
            raise ValidationException("Invalid credentials -2")
        return self._to_read_dto(user)


    def forgot_password(self, dto: ForgotPasswordDTO) -> None:
        user = self.user_repository.get_active_by_username_or_email(dto.identifier)
        if not user:
            return

        user.set_reset_password_token(expires_minutes=current_app.config["RESET_PASSWORD_EXPIRATION_MINUTES"])
        self.user_repository.save(user)

        resset_link = f"http://frontend/reset-password?token={user.reset_password_token}"

        html = f"<html><body>Reset password link: {resset_link}</body></html>"

        self.email_service.send_email(
            to=user.email,
            subject="Reset password",
            html=html,
        )

    def reset_password(self, dto: ResetPasswordDTO) -> None:
        user = self.user_repository.get_by_reset_password_token(dto.token)
        if not user or not user.is_token_rest_password_valid(dto.token):
            raise NotFoundException("Invalid or expired token")

        user.reset_password(dto.new_password)
        self.user_repository.save(user)

    def enable_mfa(self, dto: EnableMfaDTO) -> MfaSetupDTO:
        user = self.user_repository.get_user_by_id(dto.user_id)
        if not user:
            raise NotFoundException("User not found")

        secret = pyotp.random_base32()
        user.enable_mfa_secret(secret=secret)
        self.user_repository.save(user)

        toto = pyotp.TOTP(secret)

        provisioning_uri = toto.provisioning_uri(
            name=user.email,
            issuer_name="Course Management System",
        )

        qr = qrcode.QRCode(box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buf =io.BytesIO()

        img.save(buf, format="PNG")

        qr_code_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        return MfaSetupDTO(
            user_id=str(user.id),
            provisioning_uri=provisioning_uri,
            qr_code_base64=qr_code_base64,
        )



    def _to_read_dto(self, user: User) -> ReadUserDTO:
        return ReadUserDTO(
            id=str(user.id),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=GenderType(user.gender),
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,

        )

    def _send_email_with_activation_code(
            self,
            to: str,
            subject: str,
            username: str,
            activation_code: str,
    ) -> None:
        html = f'''
                    <p>Hello {username}!</p>
                    <p>Activation code: {activation_code}</p>
                '''
        self.email_service.send_email(to=to, subject=subject, html=html)