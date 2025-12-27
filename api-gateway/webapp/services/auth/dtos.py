from dataclasses import dataclass

@dataclass(frozen=True)
class LoginDTO:
    identifier: str
    password: str

@dataclass(frozen=True)
class TokenPairDTO:
    access_token: str
    refresh_token: str

@dataclass(frozen=True)
class VerifyMfaDTO:
    user_id: str
    code: str

@dataclass(frozen=True)
class LoginMfaRequiredDTO:
    mfa_required: bool
    user_id: str


