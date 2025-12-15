from .schemas import LoginSchema, TokenPairSchema
from webapp.services.auth.dtos import LoginDTO, TokenPairDTO

def to_dto_login(schema: LoginSchema) -> LoginDTO:
    return LoginDTO(identifier=schema.identifier, password=schema.password)

def to_schema_token_pair(dto: TokenPairDTO) -> TokenPairSchema:
    return TokenPairSchema(access_token=dto.access_token, refresh_token=dto.refresh_token)