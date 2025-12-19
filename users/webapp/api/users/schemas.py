from typing import Literal, Self

from pydantic import BaseModel, EmailStr, model_validator, Field

from webapp.database.models.user import GenderType


class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    first_name: str = Field(..., min_length=3, max_length=64)
    last_name: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)
    password_confirmation: str = Field(..., min_length=6)
    gender: GenderType
    role: Literal["user", "admin"]

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if self.password != self.password_confirmation:
            raise ValueError("Passwords don't match")
        return self

class ActivationCodeSchema(BaseModel):
    code: str = Field(..., min_length=1, max_length=255)


class UserResponseSchema(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    gender: GenderType
    role: Literal["user", "admin"]
    is_active: bool

class LoginSchema(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6)

class ForgotPasswordSchema(BaseModel):
    identifier: str = Field(..., min_length=3)

class ResetPasswordSchema(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)

class EnableMfaSchema(BaseModel):
    user_id: str

class MfaSetupSchema(BaseModel):
    user_id: str
    provisioning_uri: str
    qr_code_base64: str
