from datetime import timezone, datetime, timedelta
from webapp.database.models.user import User
from mongoengine.queryset.visitor import Q
import uuid

class UserRepository:
    """
    Repository class for managing User objects in the database.

    Provides methods to create, update, retrieve, and delete users
    using various query parameters.
    """

    def create_user(self, user: User) -> User:
        """
        Saves a new user to the database.

        Args:
            user (User): The User instance to create.

        Returns:
            User: The created User instance.
        """
        user.save()
        return user

    def save(self, user: User) -> User:
        """
        Updates an existing user in the database.

        Sets the updated_at timestamp to current UTC time before saving.

        Args:
            user (User): The User instance to save.

        Returns:
            User: The updated User instance.
        """
        user.updated_at = datetime.now(timezone.utc)
        user.save()
        return user

    def get_by_id(self, user_id: str) -> User | None:
        """
        Retrieves a user by their ID.

        Args:
            user_id (str): The unique ID of the user.

        Returns:
            User | None: The User instance if found, else None.
        """
        return User.objects(id=user_id).first()

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieves a user by their email.

        Args:
            email (str): The email address of the user.

        Returns:
            User | None: The User instance if found, else None.
        """
        return User.objects(email=email).first()

    def get_by_username(self, username: str) -> User | None:
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The User instance if found, else None.
        """
        return User.objects(username=username).first()

    def get_by_username_or_email(self, identifier: str) -> User | None:
        """
        Retrieves a user by either username or email.

        Args:
            identifier (str): Username or email.

        Returns:
            User | None: The User instance if found, else None.
        """
        return User.objects(Q(username=identifier) | Q(email=identifier)).first()

    def get_active_by_username_or_email(self, identifier: str) -> User | None:
        """
        Retrieves an active user by either username or email.

        Args:
            identifier (str): Username or email.

        Returns:
            User | None: The active User instance if found, else None.
        """
        return User.objects(Q(username=identifier) | Q(email=identifier), is_active=True).first()

    def get_by_activation_code(self, activation_code: str) -> User | None:
        """
        Retrieves a user by their activation code.

        Args:
            activation_code (str): The activation code.

        Returns:
            User | None: The User instance if found, else None.
        """
        return User.objects(activation_code=activation_code).first()

    def get_by_reset_password_token(self, token: str) -> User | None:
        """
        Retrieves a user by their password reset token.

        Args:
            token (str): The reset password token.

        Returns:
            User | None: The User instance if found, else None.
        """
        return User.objects(reset_password_token=token).first()

    def delete_user_by_id(self, user_id: str) -> bool:
        """
        Deletes a user by their ID.

        Args:
            user_id (str): The unique ID of the user.

        Returns:
            bool: True if user was deleted, False if not found.
        """
        user = User.objects(id=user_id).first()
        if user is None:
            return False
        user.delete()
        return True

    def delete_user_by_identifier(self, identifier: str) -> bool:
        """
        Deletes a user by username or email.

        Args:
            identifier (str): Username or email of the user.

        Returns:
            bool: True if user was deleted, False if not found.
        """
        user = self.get_by_username_or_email(identifier)
        if not user:
            return False
        user.delete()
        return True