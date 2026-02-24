from mongoengine import Document, StringField, BooleanField, DateTimeField, EmailField, EnumField
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
from enum import Enum as PyEnum
from typing import Literal
import uuid

class GenderType(PyEnum):
    """
    Enum representing the gender of a user.

    Values:
        MALE: Male
        FEMALE: Female
    """
    MALE = "Male"
    FEMALE = "Female"

class User(Document):
    """
    User model representing a system user.

    Stores personal information, email, password, role, account activation status,
    MFA secrets, and password reset tokens.

    Attributes:
        username (str): Unique username.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Unique email address.
        gender (GenderType): Gender of the user.
        password_hash (str): Hashed password.
        role (Literal["user", "admin"]): User role.
        is_active (bool): Account activation status.
        activation_code (str): Code used for account activation.
        activation_created_at (datetime): Timestamp when activation code was created.
        mfa_secret (str | None): Secret key for multi-factor authentication.
        reset_password_token (str | None): Token for password reset.
        reset_password_expires_at (datetime | None): Expiration timestamp for reset token.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp of the last update.
    """
    meta = {"collection": "users"}

    username: str = StringField(required=True, unique=True, max_length=64)
    first_name: str = StringField(required=True, max_length=64)
    last_name: str = StringField(required=True, max_length=64)
    email: str = EmailField(required=True, unique=True, max_length=255)
    gender: PyEnum = EnumField(GenderType)
    password_hash: str = StringField(required=True)
    role: Literal["user", "admin"] = StringField(default="user", choices=["user", "admin"])
    is_active: bool = BooleanField(default=False, index=True)

    activation_code: str = StringField(required=True, unique=True)
    activation_created_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))

    mfa_secret: str | None = StringField(default=None)

    reset_password_token: str | None = StringField(unique=True, sparse=True, default=None)
    reset_password_expires_at: datetime | None = DateTimeField(default=None)

    created_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))

    def activate(self) -> None:
        """
        Activates the user's account.

        Sets is_active to True and updates the activation_code to the user's ID.
        Updates the updated_at timestamp to current UTC time.
        """
        self.is_active = True
        self.activation_code = str(self.id)
        self.updated_at = datetime.now(timezone.utc)

    def update_activation_code(self) -> None:
        """
        Generates a new unique activation code for the user.

        Updates activation_created_at and updated_at timestamps to current UTC time.
        """
        self.activation_code = str(uuid.uuid4())
        self.activation_created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def set_reset_password_token(self, expires_minutes: int = 15) -> None:
        """
        Sets a password reset token with an expiration time.

        Args:
            expires_minutes (int): Minutes until the token expires. Defaults to 15.
        """
        self.reset_password_token = str(uuid.uuid4())
        self.reset_password_expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        self.updated_at = datetime.now(timezone.utc)

    def clear_reset_password_token(self) -> None:
        """
        Clears the password reset token and its expiration time.
        Updates the updated_at timestamp.
        """
        self.reset_password_token = None
        self.reset_password_expires_at = None
        self.updated_at = datetime.now(timezone.utc)

    def reset_password(self, new_password: str) -> None:
        """
        Resets the user's password.

        Hashes the new password and clears any existing reset password token.

        Args:
            new_password (str): The new password to set.
        """
        self.password_hash = generate_password_hash(new_password)
        self.clear_reset_password_token()

    def is_token_rest_password_valid(self, token: str) -> bool:
        """
        Checks if a given reset password token is valid.

        Args:
            token (str): Token to validate.

        Returns:
            bool: True if the token matches and has not expired, False otherwise.
        """
        if self.reset_password_token != token:
            return False

        if not self.reset_password_expires_at:
            return False

        now_utc = datetime.now(timezone.utc)
        created_at = self.reset_password_expires_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        return created_at > now_utc

    def enable_mfa_secret(self, secret: str) -> None:
        """
        Enables MFA (multi-factor authentication) by setting a secret.

        Args:
            secret (str): The secret key for MFA.
        """
        self.mfa_secret = secret

    def disable_mfa_secret(self) -> None:
        """
        Disables MFA by clearing the secret.
        """
        self.mfa_secret = None

    def has_mfa_secret(self) -> bool:
        """
        Checks if MFA is enabled for the user.

        Returns:
            bool: True if MFA secret is set, False otherwise.
        """
        return self.mfa_secret is not None