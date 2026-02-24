from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, EmailStr


class GenderType(Enum):
    """Enumeration for user gender."""
    MALE = "Male"
    FEMALE = "Female"


class CreateUserSchema(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username (str): Username of the user (3-64 characters).
        first_name (str): First name of the user (3-64 characters).
        last_name (str): Last name of the user (3-64 characters).
        email (EmailStr): User's email address.
        password (str): User password (min 6 characters).
        password_confirmation (str): Confirmation of the password.
        gender (GenderType): Gender of the user (Male/Female).
        role (Literal["user", "admin"]): Role of the user.
    """
    username: str = Field(..., min_length=3, max_length=64)
    first_name: str = Field(..., min_length=3, max_length=64)
    last_name: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)
    password_confirmation: str = Field(..., min_length=6)
    gender: GenderType
    role: Literal["user", "admin"]


class ActivationCodeSchema(BaseModel):
    """
    Schema for activating a user account using an activation code.

    Attributes:
        code (str): Activation code sent to the user via email.
    """
    code: str = Field(..., min_length=1, max_length=255)


class UserResponseSchema(BaseModel):
    """
    Schema representing user data in API responses.

    Attributes:
        id (str): Unique user ID.
        username (str): User's username.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (EmailStr): User's email.
        gender (GenderType): User's gender.
        role (Literal["user", "admin"]): User's role.
        is_active (bool): Whether the account is active.
    """
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    gender: GenderType
    role: Literal["user", "admin"]
    is_active: bool


class ForgotPasswordSchema(BaseModel):
    """
    Schema for requesting a password reset.

    Attributes:
        identifier (str): Username or email of the user requesting password reset.
    """
    identifier: str


class ResetPasswordSchema(BaseModel):
    """
    Schema for resetting a password using a token.

    Attributes:
        token (str): Password reset token sent to the user's email.
        new_password (str): New password to set.
    """
    token: str
    new_password: str


class EnableMfaSchema(BaseModel):
    """
    Schema for enabling Multi-Factor Authentication (MFA) for a user.

    Attributes:
        user_id (str): ID of the user enabling MFA.
    """
    user_id: str


class DisableMfaSchema(BaseModel):
    """
    Schema for disabling Multi-Factor Authentication (MFA) for a user.

    Attributes:
        user_id (str): ID of the user disabling MFA.
    """
    user_id: str


class MfaSetupSchema(BaseModel):
    """
    Schema representing MFA setup details.

    Attributes:
        user_id (str): ID of the user setting up MFA.
        provisioning_uri (str): URI used by authenticator apps.
        qr_code_base64 (str): Base64-encoded QR code for MFA setup.
    """
    user_id: str
    provisioning_uri: str
    qr_code_base64: str


class ResendActivationCodeSchema(BaseModel):
    """
    Schema for resending an activation code to a user.

    Attributes:
        identifier (str): Username or email to resend the activation code to.
    """
    identifier: str


class IdentifierSchema(BaseModel):
    """
    Generic schema for identifying a user.

    Attributes:
        identifier (str): Username or email of the user.
    """
    identifier: str


class UserIdSchema(BaseModel):
    """
    Schema for operations requiring a user ID.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str


class GetMfaSchema(BaseModel):
    """
    Schema for retrieving MFA information for a user.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str


class DeleteUserByIdSchema(BaseModel):
    """
    Schema for deleting a user by ID.

    Attributes:
        user_id (str): ID of the user to delete.
    """
    user_id: str


class DeleteUserByIdentifierSchema(BaseModel):
    """
    Schema for deleting a user by identifier.

    Attributes:
        identifier (str): Username or email of the user to delete.
    """
    identifier: str