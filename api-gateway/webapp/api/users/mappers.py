from webapp.api.users.schemas import CreateUserSchema, ActivationCodeSchema, UserResponseSchema
from webapp.services.users.dtos import CreateUserDTO, ActivationUserDTO, UserDTO


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