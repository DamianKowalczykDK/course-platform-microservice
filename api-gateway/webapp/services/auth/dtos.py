from dataclasses import dataclass

@dataclass(frozen=True)
class LoginDTO:
    """
    Data Transfer Object used to authenticate a user via the API Gateway.

    Attributes:
        identifier (str): Username or email used to identify the user.
        password (str): Plain-text password provided during login.
    """
    identifier: str
    password: str


@dataclass(frozen=True)
class TokenPairDTO:
    """
    Data Transfer Object representing a pair of authentication tokens.

    Typically returned after successful authentication.

    Attributes:
        access_token (str): Short-lived JWT used to access protected resources.
        refresh_token (str): Long-lived token used to obtain a new access token.
    """
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class VerifyMfaDTO:
    """
    Data Transfer Object used to verify a user's MFA (Multi-Factor Authentication) code.

    Attributes:
        user_id (str): Identifier of the user who is completing MFA verification.
        code (str): Time-based one-time password (TOTP) provided by the user.
    """
    user_id: str
    code: str


@dataclass(frozen=True)
class LoginMfaRequiredDTO:
    """
    Data Transfer Object returned when MFA verification is required
    before completing authentication.

    Attributes:
        mfa_required (bool): Indicates whether MFA verification is required.
        user_id (str): Identifier of the user who must complete MFA verification.
    """
    mfa_required: bool
    user_id: str