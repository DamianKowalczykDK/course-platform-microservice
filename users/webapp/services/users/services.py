from datetime import datetime, timedelta, timezone

from webapp.database.models.user import User, GenderType
from webapp.database.repositories.user import UserRepository
from webapp.services.users.dtos import CreateUserDTO, ReadUserDTO, LoginUserDTO
from webapp.services.exceptions import ConflictException, NotFoundException, ValidationException
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.services.email_service import EmailService
from flask import current_app
import uuid

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

        self.user_repository.activate(user)
        return self._to_read_dto(user)

    def resend_activation_code(self, identifier: str) -> ReadUserDTO:
        user = self.user_repository.get_by_username_or_email(identifier)
        if not user:
            raise NotFoundException("Invalid username or email")
        if user.is_active:
            raise ValidationException("User already activated")

        updated_user = self.user_repository.update_activation_code(user)

        self._send_email_with_activation_code(
            subject="Your new activation code",
            to=user.email,
            username=user.username,
            activation_code=updated_user.activation_code,
        )

        return self._to_read_dto(updated_user)

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