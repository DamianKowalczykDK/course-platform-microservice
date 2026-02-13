from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, EmailStr


class GenderType(Enum):
    MALE = "Male"
    FEMALE = "Female"

class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    first_name: str = Field(..., min_length=3, max_length=64)
    last_name: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)
    password_confirmation: str = Field(..., min_length=6)
    gender: GenderType
    role: Literal["user", "admin"]

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

class ForgotPasswordSchema(BaseModel):
    identifier: str

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str

class EnableMfaSchema(BaseModel):
    user_id: str

class DisableMfaSchema(BaseModel):
    user_id: str

class MfaSetupSchema(BaseModel):
    user_id: str
    provisioning_uri: str
    qr_code_base64: str


class ResendActivationCodeSchema(BaseModel):
    identifier: str

class IdentifierSchema(BaseModel):
    identifier: str

class UserIdSchema(BaseModel):
    user_id: str

class GetMfaSchema(BaseModel):
    user_id: str

class DeleteUserByIdSchema(BaseModel):
    user_id: str

class DeleteUserByIdentifierSchema(BaseModel):
    identifier: str
