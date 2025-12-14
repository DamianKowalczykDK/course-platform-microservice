from webapp.api.users.schemas import CreateUserSchema, UserResponseSchema, LoginSchema
from webapp.services.users.dtos import CreateUserDTO, ReadUserDTO, LoginUserDTO


def to_dto_create(schema: CreateUserSchema) -> CreateUserDTO:
    return CreateUserDTO(
        username=schema.username,
        first_name=schema.first_name,
        last_name=schema.last_name,
        email=schema.email,
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
    )

def to_dto_login(schema: LoginSchema) -> LoginUserDTO:
    return LoginUserDTO(
        identifier=schema.identifier,
        password=schema.password,
    )