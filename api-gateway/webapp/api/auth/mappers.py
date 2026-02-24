from webapp.api.auth.schemas import(
    LoginSchema,
    TokenPairSchema,
    VerifyMfaSchema,
    AccessTokenSchema
)
from webapp.services.auth.dtos import(
    LoginDTO,
    TokenPairDTO,
    VerifyMfaDTO
)


def to_dto_login(schema: LoginSchema) -> LoginDTO:
    """
    Convert LoginSchema to LoginDTO.

    Args:
        schema (LoginSchema): Schema object containing user login info.

    Returns:
        LoginDTO: DTO object for authentication service.
    """
    return LoginDTO(identifier=schema.identifier, password=schema.password)


def to_schema_token_pair(dto: TokenPairDTO) -> TokenPairSchema:
    """
    Convert TokenPairDTO to TokenPairSchema.

    Args:
        dto (TokenPairDTO): DTO containing access and refresh tokens.

    Returns:
        TokenPairSchema: Schema suitable for API response.
    """
    return TokenPairSchema(access_token=dto.access_token, refresh_token=dto.refresh_token)


def to_dto_verify_mfa(schema: VerifyMfaSchema) -> VerifyMfaDTO:
    """
    Convert VerifyMfaSchema to VerifyMfaDTO.

    Args:
        schema (VerifyMfaSchema): Schema containing user_id and MFA code.

    Returns:
        VerifyMfaDTO: DTO for verifying MFA in AuthService.
    """
    return VerifyMfaDTO(user_id=schema.user_id, code=schema.code)


def to_schema_access_token(dto: TokenPairDTO) -> AccessTokenSchema:
    """
    Extract access token from TokenPairDTO for API response.

    Args:
        dto (TokenPairDTO): DTO containing access and refresh tokens.

    Returns:
        AccessTokenSchema: Schema containing only the access token.
    """
    return AccessTokenSchema(access_token=dto.access_token)