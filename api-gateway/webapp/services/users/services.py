from webapp.services.users.dtos import (
    CreateUserDTO,
    UserDTO,
    ActivationUserDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO,
    EnableMfaDTO,
    MfaSetupDTO,
    UserIdDTO,
    GetMfaDTO,
    ResendActivationCodeDTO,
    IdentifierDTO,
    DisableMfaDTO,
    DeleteUserByIdDTO,
    DeleteUserByIdentifierDTO
)
from flask import current_app
from webapp.services.exceptions import raise_for_status
import httpx


class UserService:
    """
    Service for interacting with the Users microservice.

    Provides methods for user management including registration,
    activation, password reset, MFA, retrieval, and deletion.
    """

    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        """
        Create a new user.

        Args:
            dto (CreateUserDTO): Data transfer object containing user details.

        Returns:
            UserDTO: The created user object.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.post(f"{users_url}/", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

        return UserDTO(**response.json())

    def activate_user(self, dto: ActivationUserDTO) -> UserDTO:
        """
        Activate a user account using an activation code.

        Args:
            dto (ActivationUserDTO): DTO containing activation code.

        Returns:
            UserDTO: Activated user object.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.patch(f"{users_url}/activation", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

        return UserDTO(**response.json())

    def resend_activation_code(self, dto: ResendActivationCodeDTO) -> UserDTO:
        """
        Resend activation code to a user.

        Args:
            dto (ResendActivationCodeDTO): DTO containing user identifier.

        Returns:
            UserDTO: The user object after resending activation code.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(
            f"{users_url}/activation/resend",
            params=dto.__dict__,
            timeout=http_timeout
        )
        raise_for_status(response, not_found_message=f"User {dto.identifier} not found")

        return UserDTO(**response.json())

    def forgot_password(self, dto: ForgotPasswordDTO) -> None:
        """
        Request a password reset for a user.

        Args:
            dto (ForgotPasswordDTO): DTO containing user identifier.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.post(f"{users_url}/password/forgot", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

    def reset_password(self, dto: ResetPasswordDTO) -> None:
        """
        Reset a user's password using a valid reset token.

        Args:
            dto (ResetPasswordDTO): DTO containing reset token and new password.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.post(f"{users_url}/password/reset", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

    def enable_mfa(self, dto: EnableMfaDTO) -> MfaSetupDTO:
        """
        Enable multi-factor authentication (MFA) for a user.

        Args:
            dto (EnableMfaDTO): DTO containing user ID.

        Returns:
            MfaSetupDTO: MFA provisioning details including QR code.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.patch(f"{users_url}/mfa/enable", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

        return MfaSetupDTO(**response.json())

    def get_user_by_id(self, dto: UserIdDTO) -> UserDTO:
        """
        Retrieve a user by their ID.

        Args:
            dto (UserIdDTO): DTO containing user ID.

        Returns:
            UserDTO: User object.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{users_url}/id", params=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

        return UserDTO(**response.json())

    def get_user_by_identifier(self, dto: IdentifierDTO) -> UserDTO:
        """
        Retrieve a user by username or email.

        Args:
            dto (IdentifierDTO): DTO containing username or email.

        Returns:
            UserDTO: User object.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(
            f"{users_url}/identifier",
            params=dto.__dict__,
            timeout=http_timeout
        )
        raise_for_status(response, not_found_message=f"User {dto.identifier} not found")

        return UserDTO(**response.json())

    def disable_mfa(self, dto: DisableMfaDTO) -> UserDTO:
        """
        Disable multi-factor authentication (MFA) for a user.

        Args:
            dto (DisableMfaDTO): DTO containing user ID.

        Returns:
            UserDTO: User object after MFA is disabled.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.patch(f"{users_url}/mfa/disable", json=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

        return UserDTO(**response.json())

    def get_mfa_qr_code(self, dto: GetMfaDTO) -> MfaSetupDTO:
        """
        Retrieve the MFA QR code for a user.

        Args:
            dto (GetMfaDTO): DTO containing user ID.

        Returns:
            MfaSetupDTO: MFA provisioning details including QR code.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.get(f"{users_url}/mfa/qr", params=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

        return MfaSetupDTO(**response.json())

    def delete_user_by_id(self, dto: DeleteUserByIdDTO) -> None:
        """
        Delete a user by their ID.

        Args:
            dto (DeleteUserByIdDTO): DTO containing user ID.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.delete(f"{users_url}/id", params=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)

    def delete_user_by_identifier(self, dto: DeleteUserByIdentifierDTO) -> None:
        """
        Delete a user by username or email.

        Args:
            dto (DeleteUserByIdentifierDTO): DTO containing username or email.
        """
        users_url = current_app.config["USERS_SERVICE_URL"]
        http_timeout = current_app.config["HTTP_TIMEOUT"]

        response = httpx.delete(f"{users_url}/identifier", params=dto.__dict__, timeout=http_timeout)
        raise_for_status(response)