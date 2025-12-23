
from flask import request, jsonify
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import Provide, inject
from webapp.api.users.schemas import (
    CreateUserSchema,
    ActivationCodeSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    DisableMfaSchema,
    EnableMfaSchema,
    UserIDSchema, IdentifierSchema, ResendActivationCodeSchema

)
from webapp.api.users.mappers import (
    to_schema_user,
    to_dto_create,
    to_dto_login,
    to_dto_forgot_password,
    to_dto_reset_passwort,
    to_dto_mfa_enable,
    to_schema_mfa_setup,
    to_dto_mfa_disable,
    to_dto_get_mfa_qrcode,
    to_dto_user_id,
    to_dto_identifier, to_dto_resend_activation_code
)
from webapp.services.users.services import UserService
from webapp.container import Container
from . import users_bp

@users_bp.post("/")#type: ignore
@inject
def create_user(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = CreateUserSchema.model_validate(request.get_json() or {})
    dto = to_dto_create(payload)
    read_dto = user_service.create_user(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 201


@users_bp.patch("/activate")#type: ignore
@inject
def activate_code(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ActivationCodeSchema.model_validate(request.get_json() or {})
    read_dto = user_service.activate_user(payload.code)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200

@users_bp.get("/resend-activation")#type: ignore
@inject
def resend_activation(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ResendActivationCodeSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_resend_activation_code(payload)
    read_dto = user_service.resend_activation_code(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.get("/by-identifier")#type: ignore
@inject
def get_user_by_identifier(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = IdentifierSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_identifier(payload)
    read_dto = user_service.get_by_username_or_email(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200

@users_bp.get("/by-id")#type: ignore
@inject
def get_user_by_id(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = UserIDSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_user_id(payload)
    read_dto = user_service.get_by_id(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200

@users_bp.post("/login")#type: ignore
@inject
def verify_login(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = LoginSchema.model_validate(request.get_json() or {})
    dto = to_dto_login(payload)
    read_dto = user_service.verify_credentials(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.post("/forgot-password")#type: ignore
@inject
def forgot_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ForgotPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_forgot_password(payload)
    user_service.forgot_password(dto)
    return jsonify({"message": "If the email exist, a reset link has been sent."}), 200

@users_bp.post("/reset-password")#type: ignore
@inject
def reset_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ResetPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_reset_passwort(payload)
    user_service.reset_password(dto)
    return jsonify({"message": "Password has been reset successfully."}), 200

@users_bp.patch("/enable-mfa")#type: ignore
@inject
def enable_mfa(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = EnableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_mfa_enable(payload)
    result = user_service.enable_mfa(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200

@users_bp.patch("/disable-mfa")#type: ignore
@inject
def disable_mfa(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = DisableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_mfa_disable(payload)
    result = user_service.disable_mfa(dto)
    return jsonify(to_schema_user(result).model_dump(mode="json")), 200

@users_bp.get("/mfa-qr")#type: ignore
@inject
def get_mfa_qrcode(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = UserIDSchema.model_validate(request.args.to_dict(flat=True))
    dto = to_dto_get_mfa_qrcode(payload)
    result = user_service.get_mfa_qrcode(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200