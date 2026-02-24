from typing import Literal, Self
from pydantic import (
    BaseModel,
    EmailStr,
    model_validator,
    Field,
    field_validator
)
from webapp.database.models.user import GenderType
import re

class CreateUserSchema(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username (str): The username of the user (3-64 characters).
        first_name (str): First name of the user (3-64 characters).
        last_name (str): Last name of the user (3-64 characters).
        email (EmailStr): Valid email address.
        password (str): Password meeting complexity requirements.
        password_confirmation (str): Must match `password`.
        gender (GenderType): Gender of the user.
        role (Literal['user', 'admin']): Role assigned to the user.
    """
    username: str = Field(..., min_length=3, max_length=64)
    first_name: str = Field(..., min_length=3, max_length=64)
    last_name: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirmation: str = Field(..., min_length=8)
    gender: GenderType
    role: Literal["user", "admin"]

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Validates password complexity.

        Requirements:
            - At least 1 uppercase letter
            - At least 1 lowercase letter
            - At least 1 digit
            - At least 1 special character
            - Minimum 8 characters
        """
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'

        if not re.match(pattern, value):
            raise ValueError(
                "Password must have at least 1 uppercase, 1 lowercase, 1 digit, "
                "1 special char, and be at least 8 characters long"
            )
        return value

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        """
        Ensures that password and password_confirmation match.
        """
        if self.password != self.password_confirmation:
            raise ValueError("Passwords don't match")
        return self

class ActivationCodeSchema(BaseModel):
    """
    Schema for user activation via code.

    Attributes:
        code (str): Activation code (1-255 characters).
    """
    code: str = Field(..., min_length=1, max_length=255)

class UserResponseSchema(BaseModel):
    """
    Schema for returning user details in responses.

    Attributes:
        id (str): User ID.
        username (str): User's username.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (EmailStr): User's email address.
        gender (GenderType): User's gender.
        role (Literal['user', 'admin']): Role assigned to the user.
        is_active (bool): Whether the user account is active.
        mfa_secret (str | None): Optional MFA secret if enabled.
    """
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    gender: GenderType
    role: Literal["user", "admin"]
    is_active: bool

class LoginSchema(BaseModel):
    """
    Schema for user login request.

    Attributes:
        identifier (str): Username or email (3-64 characters).
        password (str): User's password (min 6 characters).
    """
    identifier: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6)

class ForgotPasswordSchema(BaseModel):
    """
    Schema for requesting a password reset.

    Attributes:
        identifier (str): Username or email of the user (min 3 characters).
    """
    identifier: str = Field(..., min_length=3)

class ResetPasswordSchema(BaseModel):
    """
    Schema for resetting a user's password.

    Attributes:
        token (str): Reset password token (min 1 character).
        new_password (str): New password (min 6 characters).
    """
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)

class EnableMfaSchema(BaseModel):
    """
    Schema for enabling MFA for a user.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

class DisableMfaSchema(BaseModel):
    """
    Schema for disabling MFA for a user.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

class UserIDSchema(BaseModel):
    """
    Generic schema for operations requiring a user ID.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

class IdentifierSchema(BaseModel):
    """
    Generic schema for operations requiring a username or email identifier.

    Attributes:
        identifier (str): Username or email of the user.
    """
    identifier: str

class MfaSetupSchema(BaseModel):
    """
    Schema for returning MFA setup information.

    Attributes:
        user_id (str): ID of the user.
        provisioning_uri (str): Provisioning URI for MFA setup.
        qr_code_base64 (str): QR code in base64 format for MFA.
    """
    user_id: str
    provisioning_uri: str
    qr_code_base64: str

class ResendActivationCodeSchema(BaseModel):
    """
    Schema for resending an activation code.

    Attributes:
        identifier (str): Username or email of the user.
    """
    identifier: str

class DeleteUserByIdSchema(BaseModel):
    """
    Schema for deleting a user by ID.

    Attributes:
        user_id (str): ID of the user to delete.
    """
    user_id: str

class DeleteUserByIdentifierSchema(BaseModel):
    """
    Schema for deleting a user by username or email.

    Attributes:
        identifier (str): Username or email of the user to delete.
    """
    identifier: str