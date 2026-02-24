from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
from webapp.services.auth.dtos import (
    LoginDTO,
    TokenPairDTO,
    VerifyMfaDTO,
    LoginMfaRequiredDTO
)
from webapp.services.exceptions import ValidationException, raise_for_status
import httpx
import pyotp


class AuthService:
    """
    Service responsible for handling authentication logic in the API Gateway.

    This service communicates with the Users microservice to:
    - Validate user credentials
    - Check activation status
    - Handle MFA verification
    - Generate JWT access and refresh tokens

    It acts as the authentication orchestrator for the system.
    """

    def login(self, dto: LoginDTO) -> TokenPairDTO | LoginMfaRequiredDTO:
        """
        Authenticate a user using identifier and password.

        Steps:
        1. Calls Users microservice to verify credentials.
        2. Ensures the user account is active.
        3. If MFA is enabled, returns MFA-required response.
        4. Otherwise generates JWT token pair.

        Args:
            dto (LoginDTO): Login credentials (identifier and password).

        Returns:
            TokenPairDTO | LoginMfaRequiredDTO:
                - TokenPairDTO if login succeeds without MFA.
                - LoginMfaRequiredDTO if MFA verification is required.

        Raises:
            ValidationException: If the user is not active.
            ApiException: If Users service returns an error.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.post(f"{users_url}/auth/check", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

        user = response.json()
        if not user.get("is_active"):
            raise ValidationException("User is not active")

        if user.get("mfa_secret"):
            return LoginMfaRequiredDTO(mfa_required=True, user_id=user["id"])

        return self.generate_token(user["id"])

    def verify_mfa(self, dto: VerifyMfaDTO) -> TokenPairDTO:
        """
        Verify a user's MFA (TOTP) code.

        Steps:
        1. Fetch user details from Users microservice.
        2. Validate that MFA is enabled.
        3. Verify provided TOTP code.
        4. Generate JWT token pair upon successful verification.

        Args:
            dto (VerifyMfaDTO): User ID and MFA code.

        Returns:
            TokenPairDTO: Generated access and refresh tokens.

        Raises:
            ValidationException:
                - If MFA is not enabled.
                - If MFA verification fails.
            ApiException: If Users service returns an error.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{users_url}/id", params=dto.__dict__, timeout=http_timeout)

        raise_for_status(response)

        user = response.json()
        secret = user.get("mfa_secret")

        if not secret:
            raise ValidationException("Mfa is not enabled for this user")

        totp = pyotp.TOTP(secret)

        if not totp.verify(dto.code, valid_window=1):
            raise ValidationException("Mfa verification failed")

        return self.generate_token(user["id"])

    def generate_token(self, user_id: str)  -> TokenPairDTO:
        """
        Generate JWT access and refresh tokens for a given user.

        Args:
            user_id (str): Unique identifier of the authenticated user.

        Returns:
            TokenPairDTO: Object containing access and refresh tokens.
        """
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)