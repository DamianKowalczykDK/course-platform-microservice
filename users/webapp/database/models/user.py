import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum as PyEnum
from typing import Literal

from werkzeug.security import generate_password_hash
from mongoengine import Document, StringField, BooleanField, DateTimeField, EmailField, EnumField

class GenderType(PyEnum):
    MALE = "Male"
    FEMALE = "Female"

class User(Document):
    meta = {"collection": "users"}

    username: str = StringField(required=True, unique=True, max_length=64)
    first_name: str = StringField(required=True, max_length=64)
    last_name: str = StringField(required=True, max_length=64)
    email: str = EmailField(required=True, unique=True, max_length=255)
    gender: PyEnum = EnumField(GenderType)
    password_hash: str = StringField(required=True)
    role: Literal["user", "admin"] = StringField(default="user", choices=["user", "admin"])
    is_active: bool = BooleanField(default=False)

    activation_code: str = StringField(required=True, unique=True)
    activation_created_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))

    mfa_secret: str | None = StringField(default=None)

    reset_password_token: str | None = StringField(unique=True, sparse=True, default=None)
    reset_password_expires_at: datetime | None = DateTimeField(default=None)

    created_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))

    def activate(self) -> None:
        self.is_active = True
        self.activation_code = str(self.id)
        self.updated_at = datetime.now(timezone.utc)

    def update_activation_code(self) -> None:
        self.activation_code = str(uuid.uuid4())
        self.activation_created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def set_reset_password_token(self, expires_minutes: int = 15) -> None:
        self.reset_password_token = str(uuid.uuid4())
        self.reset_password_expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        self.updated_at = datetime.now(timezone.utc)

    def clear_reset_password_token(self) -> None:
        self.reset_password_token = None
        self.reset_password_expires_at = None
        self.updated_at = datetime.now(timezone.utc)

    def reset_password(self, new_password: str) -> None:
        self.password_hash = generate_password_hash(new_password)
        self.clear_reset_password_token()

    def is_token_rest_password_valid(self, token: str) -> bool:
        if self.reset_password_token != token:
            return False

        if not self.reset_password_expires_at:
            return False

        now_utc = datetime.now(timezone.utc)

        created_at = self.reset_password_expires_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        return created_at > now_utc

    def enable_mfa_secret(self, secret: str) -> None:
        self.mfa_secret = secret

    def disable_mfa_secret(self) -> None:
        self.mfa_secret = None

    def has_mfa_secret(self) -> bool:
        return self.mfa_secret is not None


