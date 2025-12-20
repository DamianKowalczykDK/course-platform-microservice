
from flask import request, jsonify
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import Provide, inject
from webapp.api.users.schemas import (
    CreateUserSchema,
    ActivationCodeSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema, MfaSetupSchema, EnableMfaSchema,

)
from webapp.api.users.mappers import (
    to_schema_user,
    to_dto_create,
    to_dto_login,
    to_dto_forgot_password,
    to_dto_reset_passwort,
    to_dto_mfa_enable, to_schema_mfa_enable,
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

@users_bp.get("/resend-activation/<string:identifier>")#type: ignore
@inject
def resend_activation(identifier: str, user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    read_dto = user_service.resend_activation_code(identifier)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.get("<string:identifier>")#type: ignore
@inject
def get_user(identifier: str, user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    read_dto = user_service.get_by_username_or_email(identifier)
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
    return jsonify(to_schema_mfa_enable(result).model_dump(mode="json")), 200
