from dependency_injector.wiring import Provide, inject
from flask import request, jsonify
from webapp.api.users.mappers import (
    to_dto_create,
    to_dto_activate,
    to_schema_user,
    to_dto_forgot_password,
    to_dto_reset_password,
    to_schema_mfa_setup,
    to_dto_enable_mfa
)
from webapp.services.users.services import UserService
from webapp.container import Container
from flask.typing import ResponseReturnValue
from .schemas import (
    CreateUserSchema,
    ActivationCodeSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    MfaSetupSchema, EnableMfaSchema
)
from . import users_bp



@users_bp.post("")
@inject
def create_user(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = CreateUserSchema.model_validate(request.get_json() or {})
    dto = to_dto_create(payload)
    user = user_service.create_user(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 201

@users_bp.patch("/activate")
@inject
def activate_user(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ActivationCodeSchema.model_validate(request.get_json() or {})
    dto = to_dto_activate(payload)
    user = user_service.activate_user(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200

@users_bp.get("/resend-activation/<string:identifier>")
@inject
def resend_activation(identifier: str, user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    user = user_service.resend_activation_code(identifier)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200

@users_bp.post("/forgot-password")
@inject
def forgot_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ForgotPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_forgot_password(payload)
    user_service.forgot_password(dto)
    return jsonify({"message": "If the email exist, a reset link has been sent."}), 200

@users_bp.post("/reset-password")
@inject
def reset_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = ResetPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_reset_password(payload)
    user_service.reset_password(dto)
    return jsonify({"message": "Password has been reset successfully."}), 200

@users_bp.patch("/enable-mfa")
@inject
def enable_mfa(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    payload = EnableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_enable_mfa(payload)
    result = user_service.enable_mfa(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200
