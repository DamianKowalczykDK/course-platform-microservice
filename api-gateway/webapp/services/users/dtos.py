from dataclasses import dataclass
from typing import Literal

from webapp.api.users.schemas import GenderType


@dataclass(frozen=True)
class CreateUserDTO:
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    password_confirmation: str
    gender: str
    role: Literal["user", "admin"]

@dataclass(frozen=True)
class ActivationUserDTO:
    code: str

@dataclass(frozen=True)
class UserDTO:
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    gender: str
    role: Literal["user", "admin"]
    is_active: bool