from dataclasses import dataclass
from typing import Literal
from webapp.database.models.user import GenderType
from datetime import datetime

@dataclass(frozen=True)
class CreateUserDTO:
    """
    Data Transfer Object for creating a new user.

    Attributes:
        username (str): Desired username.
        password (str): Plain-text password.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        gender (GenderType): Gender of the user.
        role (str): Role of the user, default is "user".
    """
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    gender: GenderType
    role: str = "user"

@dataclass(frozen=True)
class ReadUserDTO:
    """
    Data Transfer Object for reading user information.

    Attributes:
        id (str): User ID.
        username (str): Username.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address.
        gender (GenderType): Gender of the user.
        role (Literal["user", "admin"]): Role of the user.
        is_active (bool): Account activation status.
        created_at (datetime): Account creation timestamp.
        mfa_secret (str | None): MFA secret key if set.
    """
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    gender: GenderType
    role: Literal["user", "admin"]
    is_active: bool
    created_at: datetime


@dataclass(frozen=True)
class LoginUserDTO:
    """
    Data Transfer Object for logging in a user.

    Attributes:
        identifier (str): Username or email.
        password (str): Plain-text password.
    """
    identifier: str
    password: str

@dataclass(frozen=True)
class ForgotPasswordDTO:
    """
    Data Transfer Object for initiating a password reset.

    Attributes:
        identifier (str): Username or email of the user.
    """
    identifier: str

@dataclass(frozen=True)
class ResetPasswordDTO:
    """
    Data Transfer Object for resetting a password.

    Attributes:
        token (str): Reset password token.
        new_password (str): New password to set.
    """
    token: str
    new_password: str

@dataclass(frozen=True)
class EnableMfaDTO:
    """
    Data Transfer Object for enabling MFA for a user.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

@dataclass(frozen=True)
class DisableMfaDTO:
    """
    Data Transfer Object for disabling MFA for a user.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

@dataclass(frozen=True)
class GetMfaQrCodeDTO:
    """
    Data Transfer Object for retrieving the MFA QR code.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

@dataclass(frozen=True)
class MfaSetupDTO:
    """
    Data Transfer Object representing MFA setup information.

    Attributes:
        user_id (str): ID of the user.
        provisioning_uri (str): Provisioning URI for the authenticator app.
        qr_code_base64 (str): QR code in Base64 format.
    """
    user_id: str
    provisioning_uri: str
    qr_code_base64: str

@dataclass(frozen=True)
class UserIdDTO:
    """
    Data Transfer Object containing a user ID.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

@dataclass(frozen=True)
class IdentifierDTO:
    """
    Data Transfer Object containing a user identifier.

    Attributes:
        identifier (str): Username or email.
    """
    identifier: str

@dataclass(frozen=True)
class ResendActivationCodeDTO:
    """
    Data Transfer Object for resending the account activation code.

    Attributes:
        identifier (str): Username or email of the user.
    """
    identifier: str

@dataclass(frozen=True)
class DeleteUserByIdDTO:
    """
    Data Transfer Object for deleting a user by ID.

    Attributes:
        user_id (str): ID of the user.
    """
    user_id: str

@dataclass(frozen=True)
class DeleteUserByIdentifierDTO:
    """
    Data Transfer Object for deleting a user by username or email.

    Attributes:
        identifier (str): Username or email of the user.
    """
    identifier: str