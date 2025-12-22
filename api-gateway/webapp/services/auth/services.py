from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
import httpx
from webapp.services.auth.dtos import LoginDTO, TokenPairDTO, VerifyMfaDTO
from webapp.services.exceptions import ValidationException
import pyotp


class AuthService:
    def login(self, dto: LoginDTO) -> TokenPairDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]

        response = httpx.post(f"{users_url}/login", json=dto.__dict__, timeout=5)
        if response.status_code != 200:
            raise ValidationException("invalid Credentials")

        user = response.json()
        if not user.get("is_active"):
            raise ValidationException("User is not active")

        if user.get("mfa_enabled"):
            return {
                "mfa_required": True,
                "user_id": user["id"],
            }

        return self._generate_token(user["id"])

    def verify_mfa(self, dto: VerifyMfaDTO) -> TokenPairDTO:
        users_url = current_app.config["USERS_SERVICE_URL"]
        response = httpx.get(f"{users_url}/by-id/{dto.user_id}", timeout=5)

        if response.status_code != 200:
            raise ValidationException("User not found")

        user = response.json()
        secret = user.get("mfa_secret")

        if not secret:
            raise ValidationException("Mfa is not enabled for this user")

        totp = pyotp.TOTP(secret)

        if not totp.verify(dto.code, valid_window=1):
            raise ValidationException("Mfa verification failed")

        return self._generate_token(user["id"])


    def _generate_token(self, user_id: str)  -> TokenPairDTO:
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)