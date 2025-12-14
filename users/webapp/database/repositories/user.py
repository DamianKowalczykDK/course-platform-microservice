import uuid
from datetime import timezone, datetime

from webapp.database.models.user import User
from mongoengine.queryset.visitor import Q

class UserRepository:
    def create_user(self, user: User) -> User:
        user.save()
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        return User.objects(id=user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return User.objects(email=email).first()

    def get_by_username(self, username: str) -> User | None:
        return User.objects(username=username).first()

    def get_by_username_or_email(self, identifier: str) -> User | None:
        return User.objects(Q(username=identifier) | Q(email=identifier)).first()

    def get_active_by_username_or_email(self, identifier: str) -> User | None:
        return User.objects(Q(username=identifier) | Q(email=identifier), is_active=True).first()

    def get_by_activation_code(self, activation_code: str) -> User | None:
        return User.objects(activation_code=activation_code).first()

    def get_all(self) -> list[User]:
        return list(User.objects.all())

    def activate(self, user: User) -> None:
        user.is_active = True
        user.activation_code = ""
        user.updated_at = datetime.now(timezone.utc)
        user.save()

    def update_activation_code(self, user: User) -> User:
        user.activation_code = str(uuid.uuid4())
        now_utc = datetime.now(timezone.utc)
        user.activation_created_at = now_utc
        user.updated_at = datetime.now(timezone.utc)
        user.save()
        return user





