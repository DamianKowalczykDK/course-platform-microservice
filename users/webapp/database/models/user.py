from datetime import datetime, timedelta, timezone
from enum import Enum as PyEnum
from typing import Literal

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
    created_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = DateTimeField(default=lambda: datetime.now(timezone.utc))
