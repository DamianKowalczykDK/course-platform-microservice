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
from webapp.services.exceptions import raise_for_status
import httpx

class UserService:

    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.post(f"{users_url}/", json=dto.__dict__, timeout=5)
        raise_for_status(response)

        return UserDTO(**response.json())

    def activate_user(self, dto: ActivationUserDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.patch(f"{users_url}/activation", json=dto.__dict__, timeout=5)
        raise_for_status(response)

        return UserDTO(**response.json())

    def resend_activation_code(self, dto: ResendActivationCodeDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.get(f"{users_url}/activation/resend", params=dto.__dict__ , timeout=5)
        raise_for_status(response, not_found_message=f"User {dto.identifier} not found")

        return UserDTO(**response.json())

    def forgot_password(self, dto: ForgotPasswordDTO) -> None:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.post(f"{users_url}/password/forgot", json=dto.__dict__, timeout=5)
        raise_for_status(response)

    def reset_password(self, dto: ResetPasswordDTO) -> None:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.post(f"{users_url}/password/reset", json=dto.__dict__, timeout=5)
        raise_for_status(response)

    def enable_mfa(self, dto: EnableMfaDTO) -> MfaSetupDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.patch(f"{users_url}/mfa/enable", json=dto.__dict__, timeout=5)
        raise_for_status(response)

        return MfaSetupDTO(**response.json())

    def get_user_by_id(self, dto: UserIdDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.get(f"{users_url}/id", params=dto.__dict__, timeout=5)
        raise_for_status(response)

        return UserDTO(**response.json())

    def get_user_by_identifier(self, dto: IdentifierDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.get(f"{users_url}/identifier",params=dto.__dict__ , timeout=5)
        raise_for_status(response, not_found_message=f"User {dto.identifier} not found")

        return UserDTO(**response.json())


    def disable_mfa(self, dto: DisableMfaDTO) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.patch(f"{users_url}/mfa/disable", json=dto.__dict__, timeout=5)
        raise_for_status(response)

        return UserDTO(**response.json())

    def get_qr_code(self, dto: GetMfaDTO) -> MfaSetupDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.get(f"{users_url}/mfa/qr", params=dto.__dict__, timeout=5)
        raise_for_status(response)

        return MfaSetupDTO(**response.json())
