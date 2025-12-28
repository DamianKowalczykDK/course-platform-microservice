from dependency_injector.wiring import Provide, inject
from flask import request, jsonify
from webapp.api.users.mappers import (
    to_dto_create,
    to_dto_activate,
    to_schema_user,
    to_dto_forgot_password,
    to_dto_reset_password,
    to_schema_mfa_setup,
    to_dto_enable_mfa,
    to_dto_resend_activation_code,
    to_dto_user_id,
    to_dto_identifier,
    to_dto_disable_mfa,
    to_dto_mfa_qr
)
from webapp.services.users.services import UserService
from webapp.container import Container
from flask.typing import ResponseReturnValue
from .schemas import (
    CreateUserSchema,
    ActivationCodeSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    EnableMfaSchema,
    ResendActivationCodeSchema,
    UserIdSchema,
    IdentifierSchema,
    DisableMfaSchema,
    GetMfaSchema

)
from . import users_bp


@users_bp.post("")
@inject
def create_user(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = CreateUserSchema.model_validate(request.get_json() or {})
    dto = to_dto_create(payload)
    user = user_service.create_user(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 201

@users_bp.get("/id")
@inject
def get_user_by_id(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = UserIdSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_user_id(payload)
    user = user_service.get_user_by_id(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200

@users_bp.get("/identifier")
@inject
def get_user_by_identifier(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = IdentifierSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_identifier(payload)
    user = user_service.get_user_by_identifier(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200


@users_bp.patch("/activation")
@inject
def activate_user(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ActivationCodeSchema.model_validate(request.get_json() or {})
    dto = to_dto_activate(payload)
    user = user_service.activate_user(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200

@users_bp.get("/activation/resend")
@inject
def resend_activation( user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ResendActivationCodeSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_resend_activation_code(payload)
    user = user_service.resend_activation_code(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200

@users_bp.post("/password/forgot")
@inject
def forgot_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ForgotPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_forgot_password(payload)
    user_service.forgot_password(dto)
    return jsonify({"message": "If the email exist, a reset link has been sent."}), 200

@users_bp.post("/password/reset")
@inject
def reset_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ResetPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_reset_password(payload)
    user_service.reset_password(dto)
    return jsonify({"message": "Password has been reset successfully."}), 200

@users_bp.patch("/mfa/enable")
@inject
def enable_mfa(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = EnableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_enable_mfa(payload)
    result = user_service.enable_mfa(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200

@users_bp.patch("/mfa/disable")
@inject
def disable_mfa(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = DisableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_disable_mfa(payload)
    result = user_service.disable_mfa(dto)
    return jsonify(to_schema_user(result).model_dump(mode="json")), 200

@users_bp.get("/mfa/qr")
@inject
def get_mfa_qr_code(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = GetMfaSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_mfa_qr(payload)
    result = user_service.get_mfa_qr_code(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json"), 200)