from webapp.api.users.schemas import (
    CreateUserSchema,
    UserResponseSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    MfaSetupSchema,
    EnableMfaSchema,
    DisableMfaSchema,
    UserIDSchema,
    IdentifierSchema,
    ResendActivationCodeSchema,
    DeleteUserByIdSchema,
    DeleteUserByIdentifierSchema
)
from webapp.services.users.dtos import (
    CreateUserDTO,
    ReadUserDTO,
    LoginUserDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO,
    MfaSetupDTO,
    EnableMfaDTO,
    DisableMfaDTO,
    GetMfaQrCodeDTO,
    UserIdDTO,
    IdentifierDTO,
    ResendActivationCodeDTO,
    DeleteUserByIdDTO,
    DeleteUserByIdentifierDTO
)

def to_dto_create(schema: CreateUserSchema) -> CreateUserDTO:
    """
    Converts a CreateUserSchema to CreateUserDTO.

    Args:
        schema (CreateUserSchema): Input schema from API request.

    Returns:
        CreateUserDTO: DTO for service layer.
    """
    return CreateUserDTO(
        username=schema.username,
        first_name=schema.first_name,
        last_name=schema.last_name,
        email=str(schema.email),
        gender=schema.gender,
        role=schema.role,
        password=schema.password,
    )

def to_schema_user(dto: ReadUserDTO) -> UserResponseSchema:
    """
    Converts a ReadUserDTO to UserResponseSchema.

    Args:
        dto (ReadUserDTO): DTO from service layer.

    Returns:
        UserResponseSchema: Schema for API response.
    """
    return UserResponseSchema(
        id=dto.id,
        username=dto.username,
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        gender=dto.gender,
        role=dto.role,
        is_active=dto.is_active,

    )

def to_dto_login(schema: LoginSchema) -> LoginUserDTO:
    """
    Converts a LoginSchema to LoginUserDTO.

    Args:
        schema (LoginSchema): Input schema from API request.

    Returns:
        LoginUserDTO: DTO for service layer.
    """
    return LoginUserDTO(
        identifier=schema.identifier,
        password=schema.password,
    )

def to_dto_forgot_password(schema: ForgotPasswordSchema) -> ForgotPasswordDTO:
    """
    Converts a ForgotPasswordSchema to ForgotPasswordDTO.

    Args:
        schema (ForgotPasswordSchema): Input schema from API request.

    Returns:
        ForgotPasswordDTO: DTO for service layer.
    """
    return ForgotPasswordDTO(identifier=schema.identifier)

def to_dto_reset_password(schema: ResetPasswordSchema) -> ResetPasswordDTO:
    """
    Converts a ResetPasswordSchema to ResetPasswordDTO.

    Args:
        schema (ResetPasswordSchema): Input schema from API request.

    Returns:
        ResetPasswordDTO: DTO for service layer.
    """
    return ResetPasswordDTO(token=schema.token, new_password=schema.new_password)

def to_schema_mfa_setup(dto: MfaSetupDTO) -> MfaSetupSchema:
    """
    Converts a MfaSetupDTO to MfaSetupSchema.

    Args:
        dto (MfaSetupDTO): DTO from service layer.

    Returns:
        MfaSetupSchema: Schema for API response.
    """
    return MfaSetupSchema(user_id=dto.user_id, provisioning_uri=dto.provisioning_uri, qr_code_base64=dto.qr_code_base64)

def to_dto_mfa_enable(schema: EnableMfaSchema) -> EnableMfaDTO:
    """
    Converts an EnableMfaSchema to EnableMfaDTO.

    Args:
        schema (EnableMfaSchema): Input schema from API request.

    Returns:
        EnableMfaDTO: DTO for service layer.
    """
    return EnableMfaDTO(
        user_id=schema.user_id,
    )

def to_dto_mfa_disable(schema: DisableMfaSchema) -> DisableMfaDTO:
    """
    Converts a DisableMfaSchema to DisableMfaDTO.

    Args:
        schema (DisableMfaSchema): Input schema from API request.

    Returns:
        DisableMfaDTO: DTO for service layer.
    """
    return DisableMfaDTO(user_id=schema.user_id)

def to_dto_get_mfa_qrcode(schema: UserIDSchema) -> GetMfaQrCodeDTO:
    """
    Converts a UserIDSchema to GetMfaQrCodeDTO.

    Args:
        schema (UserIDSchema): Input schema from API request.

    Returns:
        GetMfaQrCodeDTO: DTO for service layer.
    """
    return GetMfaQrCodeDTO(user_id=schema.user_id)

def to_dto_user_id(schema: UserIDSchema) -> UserIdDTO:
    """
    Converts a UserIDSchema to UserIdDTO.

    Args:
        schema (UserIDSchema): Input schema from API request.

    Returns:
        UserIdDTO: DTO for service layer.
    """
    return UserIdDTO(user_id=schema.user_id)

def to_dto_identifier(schema: IdentifierSchema) -> IdentifierDTO:
    """
    Converts an IdentifierSchema to IdentifierDTO.

    Args:
        schema (IdentifierSchema): Input schema from API request.

    Returns:
        IdentifierDTO: DTO for service layer.
    """
    return IdentifierDTO(identifier=schema.identifier)

def to_dto_resend_activation_code(schema: ResendActivationCodeSchema) -> ResendActivationCodeDTO:
    """
    Converts a ResendActivationCodeSchema to ResendActivationCodeDTO.

    Args:
        schema (ResendActivationCodeSchema): Input schema from API request.

    Returns:
        ResendActivationCodeDTO: DTO for service layer.
    """
    return ResendActivationCodeDTO(identifier=schema.identifier)

def to_dto_delete_user_by_id(schema: DeleteUserByIdSchema) -> DeleteUserByIdDTO:
    """
    Converts a DeleteUserByIdSchema to DeleteUserByIdDTO.

    Args:
        schema (DeleteUserByIdSchema): Input schema from API request.

    Returns:
        DeleteUserByIdDTO: DTO for service layer.
    """
    return DeleteUserByIdDTO(user_id=schema.user_id)

def to_dto_delete_user_by_identifier(schema: DeleteUserByIdentifierSchema) -> DeleteUserByIdentifierDTO:
    """
    Converts a DeleteUserByIdentifierSchema to DeleteUserByIdentifierDTO.

    Args:
        schema (DeleteUserByIdentifierSchema): Input schema from API request.

    Returns:
        DeleteUserByIdentifierDTO: DTO for service layer.
    """
    return DeleteUserByIdentifierDTO(identifier=schema.identifier)