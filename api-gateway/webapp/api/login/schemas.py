from pydantic import BaseModel

class LoginSchema(BaseModel):
    identifier: str
    password: str

class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str