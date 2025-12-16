from webapp.services.users.dtos import CreateUserDTO, UserDTO, ActivationUserDTO
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

    def resend_activation_code(self, identifier: str) -> UserDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.get(f"{users_url}/resend-activation/{identifier}", timeout=5)

        if response.status_code == 404:
            raise NotFoundException(f"User {identifier} not found")

        if response.status_code != 200:
            raise ValidationException(f"Failed to resend activation code {response.text}")

        return UserDTO(**response.json())