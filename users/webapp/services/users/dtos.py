from dataclasses import dataclass
from typing import Literal

from webapp.database.models.user import GenderType
from datetime import datetime

@dataclass(frozen=True)
class CreateUserDTO:
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    gender: GenderType
    role: str = "user"

@dataclass(frozen=True)
class ReadUserDTO:
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    gender: GenderType
    role: Literal["user", "admin"]
    is_active: bool
    created_at: datetime
    mfa_secret: str | None = None

@dataclass(frozen=True)
class LoginUserDTO:
    identifier: str
    password: str

@dataclass(frozen=True)
class ForgotPasswordDTO:
    identifier: str

@dataclass(frozen=True)
class ResetPasswordDTO:
    token: str
    new_password: str