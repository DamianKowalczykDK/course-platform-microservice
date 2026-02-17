from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
from webapp.services.auth.dtos import LoginDTO, TokenPairDTO, VerifyMfaDTO, LoginMfaRequiredDTO
from webapp.services.exceptions import ValidationException, raise_for_status
import httpx
import pyotp


class AuthService:
    def __init__(self) -> None:
        self.users_url = current_app.config["USERS_SERVICE_URL"]
        self.http_timeout = current_app.config["HTTP_TIMEOUT"]

    def login(self, dto: LoginDTO) -> TokenPairDTO | LoginMfaRequiredDTO:
        response = httpx.post(f"{self.users_url}/auth/check", json=dto.__dict__, timeout=self.http_timeout)
        raise_for_status(response)

        user = response.json()
        if not user.get("is_active"):
            raise ValidationException("User is not active")

        if user.get("mfa_secret"):
            return LoginMfaRequiredDTO(mfa_required=True, user_id=user["id"])

        return self.generate_token(user["id"])

    def verify_mfa(self, dto: VerifyMfaDTO) -> TokenPairDTO:
        response = httpx.get(f"{self.users_url}/id", params=dto.__dict__, timeout=self.http_timeout)

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
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        return TokenPairDTO(access_token=access_token, refresh_token=refresh_token)