from webapp.api.users.schemas import (
    CreateUserSchema,
    ActivationCodeSchema,
    UserResponseSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    MfaSetupSchema,
    EnableMfaSchema
)
from webapp.services.users.dtos import (
    CreateUserDTO,
    ActivationUserDTO,
    UserDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO,
    MfaSetupDTO,
    EnableMfaDTO
)

def to_dto_create(schema: CreateUserSchema) -> CreateUserDTO:
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
    return ActivationUserDTO(code=schema.code)

def to_schema_user(dto: UserDTO) -> UserResponseSchema:
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
    return ForgotPasswordDTO(identifier=schema.identifier)

def to_dto_reset_password(schema: ResetPasswordSchema) -> ResetPasswordDTO:
    return ResetPasswordDTO(token=schema.token, new_password=schema.new_password)

def to_dto_enable_mfa(schema: EnableMfaSchema) -> EnableMfaDTO:
    return EnableMfaDTO(user_id=schema.user_id)

def to_schema_mfa_setup(dto: MfaSetupDTO) -> MfaSetupSchema:
    return MfaSetupSchema(
        user_id=dto.user_id,
        provisioning_uri=dto.provisioning_uri,
        qr_code_base64=dto.qr_code_base64,
    )