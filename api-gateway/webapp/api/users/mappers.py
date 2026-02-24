from webapp.api.users.schemas import (
    CreateUserSchema,
    ActivationCodeSchema,
    UserResponseSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    MfaSetupSchema,
    EnableMfaSchema,
    ResendActivationCodeSchema,
    IdentifierSchema,
    UserIdSchema,
    DisableMfaSchema,
    GetMfaSchema,
    DeleteUserByIdSchema,
    DeleteUserByIdentifierSchema
)
from webapp.services.users.dtos import (
    CreateUserDTO,
    ActivationUserDTO,
    UserDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO,
    MfaSetupDTO,
    EnableMfaDTO,
    ResendActivationCodeDTO,
    IdentifierDTO,
    UserIdDTO,
    GetMfaDTO,
    DisableMfaDTO,
    DeleteUserByIdDTO,
    DeleteUserByIdentifierDTO
)


def to_dto_create(schema: CreateUserSchema) -> CreateUserDTO:
    """
    Convert CreateUserSchema to CreateUserDTO.

    Args:
        schema (CreateUserSchema): Input Pydantic schema from request.

    Returns:
        CreateUserDTO: DTO for service layer processing.
    """
    return CreateUserDTO(
        username=schema.username,
        first_name=schema.first_name,
        last_name=schema.last_name,
        email=str(schema.email),
        password=schema.password,
        password_confirmation=schema.password_confirmation,
        gender=schema.gender.value,
        role=schema.role,
    )


def to_dto_activate(schema: ActivationCodeSchema) -> ActivationUserDTO:
    """
    Convert ActivationCodeSchema to ActivationUserDTO.

    Args:
        schema (ActivationCodeSchema): Input schema containing activation code.

    Returns:
        ActivationUserDTO: DTO for activating user in service layer.
    """
    return ActivationUserDTO(code=schema.code)


def to_schema_user(dto: UserDTO) -> UserResponseSchema:
    """
    Convert UserDTO to UserResponseSchema.

    Args:
        dto (UserDTO): DTO from service layer.

    Returns:
        UserResponseSchema: Schema for returning user data in response.
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


def to_dto_forgot_password(schema: ForgotPasswordSchema) -> ForgotPasswordDTO:
    """
    Convert ForgotPasswordSchema to ForgotPasswordDTO.

    Args:
        schema (ForgotPasswordSchema): Input schema with user identifier.

    Returns:
        ForgotPasswordDTO: DTO for requesting password reset.
    """
    return ForgotPasswordDTO(identifier=schema.identifier)


def to_dto_reset_password(schema: ResetPasswordSchema) -> ResetPasswordDTO:
    """
    Convert ResetPasswordSchema to ResetPasswordDTO.

    Args:
        schema (ResetPasswordSchema): Input schema with reset token and new password.

    Returns:
        ResetPasswordDTO: DTO for resetting password in service layer.
    """
    return ResetPasswordDTO(token=schema.token, new_password=schema.new_password)


def to_dto_enable_mfa(schema: EnableMfaSchema) -> EnableMfaDTO:
    """
    Convert EnableMfaSchema to EnableMfaDTO.

    Args:
        schema (EnableMfaSchema): Input schema containing user ID.

    Returns:
        EnableMfaDTO: DTO for enabling MFA in service layer.
    """
    return EnableMfaDTO(user_id=schema.user_id)


def to_schema_mfa_setup(dto: MfaSetupDTO) -> MfaSetupSchema:
    """
    Convert MfaSetupDTO to MfaSetupSchema.

    Args:
        dto (MfaSetupDTO): DTO containing MFA provisioning data.

    Returns:
        MfaSetupSchema: Schema for returning MFA setup info to client.
    """
    return MfaSetupSchema(
        user_id=dto.user_id,
        provisioning_uri=dto.provisioning_uri,
        qr_code_base64=dto.qr_code_base64,
    )


def to_dto_resend_activation_code(schema: ResendActivationCodeSchema) -> ResendActivationCodeDTO:
    """
    Convert ResendActivationCodeSchema to ResendActivationCodeDTO.

    Args:
        schema (ResendActivationCodeSchema): Input schema containing identifier.

    Returns:
        ResendActivationCodeDTO: DTO for resending activation code.
    """
    return ResendActivationCodeDTO(identifier=schema.identifier)


def to_dto_identifier(schema: IdentifierSchema) -> IdentifierDTO:
    """
    Convert IdentifierSchema to IdentifierDTO.

    Args:
        schema (IdentifierSchema): Input schema with identifier.

    Returns:
        IdentifierDTO: DTO for service operations requiring identifier.
    """
    return IdentifierDTO(identifier=schema.identifier)


def to_dto_user_id(schema: UserIdSchema) -> UserIdDTO:
    """
    Convert UserIdSchema to UserIdDTO.

    Args:
        schema (UserIdSchema): Input schema with user ID.

    Returns:
        UserIdDTO: DTO for service operations requiring user ID.
    """
    return UserIdDTO(user_id=schema.user_id)


def to_dto_disable_mfa(schema: DisableMfaSchema) -> DisableMfaDTO:
    """
    Convert DisableMfaSchema to DisableMfaDTO.

    Args:
        schema (DisableMfaSchema): Input schema containing user ID.

    Returns:
        DisableMfaDTO: DTO for disabling MFA in service layer.
    """
    return DisableMfaDTO(user_id=schema.user_id)


def to_dto_mfa_qr(schema: GetMfaSchema) -> GetMfaDTO:
    """
    Convert GetMfaSchema to GetMfaDTO.

    Args:
        schema (GetMfaSchema): Input schema with user ID.

    Returns:
        GetMfaDTO: DTO for retrieving MFA QR code.
    """
    return GetMfaDTO(user_id=schema.user_id)


def to_dto_delete_user_by_id(schema: DeleteUserByIdSchema) -> DeleteUserByIdDTO:
    """
    Convert DeleteUserByIdSchema to DeleteUserByIdDTO.

    Args:
        schema (DeleteUserByIdSchema): Input schema with user ID.

    Returns:
        DeleteUserByIdDTO: DTO for deleting a user by ID.
    """
    return DeleteUserByIdDTO(user_id=schema.user_id)


def to_dto_delete_user_by_identifier(schema: DeleteUserByIdentifierSchema) -> DeleteUserByIdentifierDTO:
    """
    Convert DeleteUserByIdentifierSchema to DeleteUserByIdentifierDTO.

    Args:
        schema (DeleteUserByIdentifierSchema): Input schema with user identifier.

    Returns:
        DeleteUserByIdentifierDTO: DTO for deleting a user by identifier.
    """
    return DeleteUserByIdentifierDTO(identifier=schema.identifier)