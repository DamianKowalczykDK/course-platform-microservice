from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
import httpx
from webapp.services.auth.dtos import LoginDTO, TokenPairDTO
from webapp.services.exceptions import ValidationException


class AuthService:
    def login(self, dto: LoginDTO) -> TokenPairDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.post(f"{users_url}/login", json=dto.__dict__, timeout=5)

        if response.status_code != 200:
            raise ValidationException("invalid Credentials")

        user = response.json()

        if not user.get("is_active"):
            raise ValidationException("User is not active")

        access_token = create_access_token(identity=user["id"])
        refresh_token = create_refresh_token(identity=user["id"])

        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)