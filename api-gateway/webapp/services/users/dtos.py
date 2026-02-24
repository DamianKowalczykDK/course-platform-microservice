from dataclasses import dataclass
from typing import Literal
from webapp.api.users.schemas import GenderType

@dataclass(frozen=True)
class CreateUserDTO:
    """
    DTO for creating a new user.

    Attributes:
        username (str): The user's username.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's password.
        password_confirmation (str): Confirmation of the password.
        gender (str): The user's gender.
        role (Literal["user", "admin"]): Role of the user.
    """
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    password_confirmation: str
    gender: str
    role: Literal["user", "admin"]

@dataclass(frozen=True)
class ActivationUserDTO:
    """DTO for user activation via code."""
    code: str

@dataclass(frozen=True)
class UserDTO:
    """
    DTO representing a user returned from the service.

    Attributes:
        id (str): Unique user ID.
        username (str): The user's username.
        first_name (str): First name.
        last_name (str): Last name.
        email (str): Email address.
        gender (GenderType): Gender type.
        role (Literal["user", "admin"]): User role.
        is_active (bool): Whether the user is active.
        mfa_secret (str): Secret for MFA, if enabled.
    """
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    gender: GenderType
    role: Literal["user", "admin"]
    is_active: bool
    mfa_secret: str

@dataclass(frozen=True)
class ForgotPasswordDTO:
    """DTO for requesting a password reset."""
    identifier: str

@dataclass(frozen=True)
class ResetPasswordDTO:
    """DTO for resetting a user's password."""
    token: str
    new_password: str

@dataclass(frozen=True)
class EnableMfaDTO:
    """DTO to enable multi-factor authentication for a user."""
    user_id: str

@dataclass(frozen=True)
class DisableMfaDTO:
    """DTO to disable multi-factor authentication for a user."""
    user_id: str

@dataclass(frozen=True)
class UserIdDTO:
    """DTO to identify a user by ID."""
    user_id: str

@dataclass(frozen=True)
class GetMfaDTO:
    """DTO to fetch MFA details for a user."""
    user_id: str

@dataclass(frozen=True)
class MfaSetupDTO:
    """
    DTO returned after MFA setup.

    Attributes:
        user_id (str): User ID.
        provisioning_uri (str): URI for TOTP provisioning.
        qr_code_base64 (str): QR code in base64 format for authenticator apps.
    """
    user_id: str
    provisioning_uri: str
    qr_code_base64: str

@dataclass(frozen=True)
class ResendActivationCodeDTO:
    """DTO to resend activation code to a user."""
    identifier: str

@dataclass(frozen=True)
class IdentifierDTO:
    """DTO to identify a user by username or email."""
    identifier: str

@dataclass(frozen=True)
class DeleteUserByIdDTO:
    """DTO to delete a user by ID."""
    user_id: str

@dataclass(frozen=True)
class DeleteUserByIdentifierDTO:
    """DTO to delete a user by username or email."""
    identifier: str