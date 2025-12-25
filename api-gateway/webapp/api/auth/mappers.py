from .schemas import LoginSchema, TokenPairSchema, VerifyMfaSchema, AccessTokenSchema
from webapp.services.auth.dtos import LoginDTO, TokenPairDTO, VerifyMfaDTO

def to_dto_login(schema: LoginSchema) -> LoginDTO:
    return LoginDTO(identifier=schema.identifier, password=schema.password)

def to_schema_token_pair(dto: TokenPairDTO) -> TokenPairSchema:
    return TokenPairSchema(access_token=dto.access_token, refresh_token=dto.refresh_token)

def to_dto_verify_mfa(schema: VerifyMfaSchema) -> VerifyMfaDTO:
    return VerifyMfaDTO(user_id=schema.user_id, code=schema.code)

def to_schema_access_token(dto: TokenPairDTO) -> AccessTokenSchema:
    return AccessTokenSchema(access_token=dto.access_token)