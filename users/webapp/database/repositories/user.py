import uuid
from datetime import timezone, datetime, timedelta

from webapp.database.models.user import User
from mongoengine.queryset.visitor import Q

class UserRepository:
    def create_user(self, user: User) -> User:
        user.save()
        return user

    def save(self, user: User) -> User:
        user.updated_at = datetime.now(timezone.utc)
        user.save()
        return user

    def get_by_id(self, user_id: str) -> User | None:
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

    def get_by_reset_password_token(self, token: str) -> User | None:
        return User.objects(reset_password_token=token).first()





