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
    return UserResponseSchema(
        id=dto.id,
        username=dto.username,
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        gender=dto.gender,
        role=dto.role,
        is_active=dto.is_active,
        mfa_secret=dto.mfa_secret,
    )

def to_dto_login(schema: LoginSchema) -> LoginUserDTO:
    return LoginUserDTO(
        identifier=schema.identifier,
        password=schema.password,
    )

def to_dto_forgot_password(schema: ForgotPasswordSchema) -> ForgotPasswordDTO:
    return ForgotPasswordDTO(identifier=schema.identifier)


def to_dto_reset_passwort(schema: ResetPasswordSchema) -> ResetPasswordDTO:
    return ResetPasswordDTO(token=schema.token, new_password=schema.new_password)

def to_schema_mfa_setup(dto: MfaSetupDTO) -> MfaSetupSchema:
    return MfaSetupSchema(user_id=dto.user_id, provisioning_uri=dto.provisioning_uri, qr_code_base64=dto.qr_code_base64)

def to_dto_mfa_enable(schema: EnableMfaSchema) -> EnableMfaDTO:
    return EnableMfaDTO(
        user_id=schema.user_id,
    )

def to_dto_mfa_disable(schema: DisableMfaSchema) -> DisableMfaDTO:
    return DisableMfaDTO(user_id=schema.user_id)

def to_dto_get_mfa_qrcode(schema: UserIDSchema) -> GetMfaQrCodeDTO:
    return GetMfaQrCodeDTO(user_id=schema.user_id)

def to_dto_user_id(schema: UserIDSchema) -> UserIdDTO:
    return UserIdDTO(user_id=schema.user_id)

def to_dto_identifier(schema: IdentifierSchema) -> IdentifierDTO:
    return IdentifierDTO(identifier=schema.identifier)

def to_dto_resend_activation_code(schema: ResendActivationCodeSchema) -> ResendActivationCodeDTO:
    return ResendActivationCodeDTO(identifier=schema.identifier)

def to_dto_delete_user_by_id(schema: DeleteUserByIdSchema) -> DeleteUserByIdDTO:
    return DeleteUserByIdDTO(user_id=schema.user_id)

def to_dto_delete_user_by_identifier(schema: DeleteUserByIdentifierSchema) -> DeleteUserByIdentifierDTO:
    return DeleteUserByIdentifierDTO(identifier=schema.identifier)