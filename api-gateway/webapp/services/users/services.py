from webapp.services.users.dtos import (
    CreateUserDTO,
    UserDTO,
    ActivationUserDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO,
    EnableMfaDTO,
    MfaSetupDTO,
    UserIdDTO, GetMfaDTO, ResendActivationCodeDTO, IdentifierDTO, DisableMfaDTO
)
from flask import current_app
from webapp.services.exceptions import ValidationException, NotFoundException
import httpx

class UserService:

    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.post(f"{users_url}/", json=dto.__dict__, timeout=5)

        if response.status_code != 201:
            raise ValidationException(f"Failed to create user {response.text}")

        return UserDTO(**response.json())

    def activate_user(self, dto: ActivationUserDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.patch(f"{users_url}/activate", json=dto.__dict__, timeout=5)

        if response.status_code != 200:
            raise ValidationException(f"Failed to activate user {response.text}")
        return UserDTO(**response.json())

    def resend_activation_code(self, dto: ResendActivationCodeDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.get(f"{users_url}/resend-activation", params=dto.__dict__ , timeout=5)

        if response.status_code == 404:
            raise NotFoundException(f"User {dto.identifier} not found")

        if response.status_code != 200:
            raise ValidationException(f"Failed to resend activation code {response.text}")

        return UserDTO(**response.json())

    def forgot_password(self, dto: ForgotPasswordDTO) -> None:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.post(f"{users_url}/forgot-password", json=dto.__dict__, timeout=5)
        if response.status_code != 200:
            raise ValidationException(f"Failed to forgot password {response.text}")

    def reset_password(self, dto: ResetPasswordDTO) -> None:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.post(f"{users_url}/reset-password", json=dto.__dict__, timeout=5)
        if response.status_code != 200:
            raise ValidationException(f"Failed to reset password {response.text}")

    def enable_mfa(self, dto: EnableMfaDTO) -> MfaSetupDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.patch(f"{users_url}/enable-mfa", json=dto.__dict__, timeout=5)
        if response.status_code != 200:
            raise ValidationException(f"Failed to enable MFA {response.text}")
        return MfaSetupDTO(**response.json())

    def get_user_by_id(self, dto: UserIdDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.get(f"{users_url}/by-id", params=dto.__dict__, timeout=5)

        if response.status_code != 200:
            raise NotFoundException(f"User {dto.user_id} not found")
        return UserDTO(**response.json())

    def get_user_by_identifier(self, dto: IdentifierDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.get(f"{users_url}/by-identifier",params=dto.__dict__ , timeout=5)

        if response.status_code == 404:
            raise NotFoundException(f"User {dto.identifier} not found")

        if response.status_code != 200:
            raise ValidationException(f"Failed to get user {response.text}")
        return UserDTO(**response.json())


    def disable_mfa(self, dto: DisableMfaDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.patch(f"{users_url}/disable-mfa", json=dto.__dict__, timeout=5)
        if response.status_code != 200:
            raise ValidationException(f"Failed to disable MFA {response.text}")

        return UserDTO(**response.json())

    def get_qr_code(self, dto: GetMfaDTO) -> MfaSetupDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.get(f"{users_url}/mfa-qr", params=dto.__dict__, timeout=5)
        if response.status_code != 200:
            raise ValidationException(f"Failed to get MFA QR code {response.text}")
        return MfaSetupDTO(**response.json())
