from pydantic import BaseModel

class LoginSchema(BaseModel):
    identifier: str
    password: str

class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str

class VerifyMfaSchema(BaseModel):
    user_id: str
    code: str