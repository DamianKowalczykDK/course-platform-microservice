from webapp.database.models.user import User
from mongoengine.queryset.visitor import Q

class UserRepository:
    def create_user(self, user: User) -> User:
        user.save()
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        return User.objects.get(id=user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return User.objects.get(email=email).first()

    def get_by_username_or_email(self, identifier: str) -> User | None:
        return User.objects(Q(username=identifier) | Q(email=identifier)).first()

    def get_by_activation_code(self, activation_code: str) -> User | None:
        return User.objects.get(activation_code=activation_code).first()

    def get_all(self) -> list[User]:
        return list(User.objects.all())

    def activate(self, user: User) -> None:
        user.is_active = True
        user.activation_code = ""
        user.save()



