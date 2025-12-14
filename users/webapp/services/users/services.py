from webapp.database.models.user import User, GenderType
from webapp.database.repositories.user import UserRepository
from webapp.services.users.dtos import CreateUserDTO, ReadUserDTO
from webapp.services.exceptions import ConflictException, NotFoundException
from werkzeug.security import generate_password_hash
import uuid

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, dto: CreateUserDTO ) -> ReadUserDTO:
        if self.user_repository.get_by_email(dto.email):
            raise ConflictException("Email already exists")

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
        return self._to_read_dto(user)

    def activate_user(self, activation_code: str) -> ReadUserDTO:
        user = self.user_repository.get_by_activation_code(activation_code)
        if user is None:
            raise NotFoundException("Invalid activation code")

        self.user_repository.activate(user)
        return self._to_read_dto(user)

    def get_by_username_or_email(self, identifier: str) -> ReadUserDTO:
        user = self.user_repository.get_by_username_or_email(identifier)
        if user is None:
            raise NotFoundException("Invalid username or email")

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