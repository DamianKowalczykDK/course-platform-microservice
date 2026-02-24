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
    UserIDSchema,
    IdentifierSchema,
    ResendActivationCodeSchema,
    DeleteUserByIdSchema,
    DeleteUserByIdentifierSchema
)
from webapp.api.users.mappers import (
    to_schema_user,
    to_dto_create,
    to_dto_login,
    to_dto_forgot_password,
    to_dto_reset_password,
    to_dto_mfa_enable,
    to_schema_mfa_setup,
    to_dto_mfa_disable,
    to_dto_get_mfa_qrcode,
    to_dto_user_id,
    to_dto_identifier,
    to_dto_resend_activation_code,
    to_dto_delete_user_by_id,
    to_dto_delete_user_by_identifier
)
from webapp.services.users.services import UserService
from webapp.container import Container
from webapp.extensions import db
from . import users_bp


@users_bp.post("/")  # type: ignore
@inject
def create_user(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to create a new user.

    Expects a JSON payload conforming to CreateUserSchema.

    Returns:
        JSON response with created user data (UserResponseSchema) and HTTP 201.
    """
    payload = CreateUserSchema.model_validate(request.get_json() or {})
    dto = to_dto_create(payload)
    read_dto = user_service.create_user(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 201


@users_bp.patch("/activation")  # type: ignore
@inject
def activate_code(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to activate a user account via activation code.

    Expects a JSON payload conforming to ActivationCodeSchema.

    Returns:
        JSON response with activated user data (UserResponseSchema) and HTTP 200.
    """
    payload = ActivationCodeSchema.model_validate(request.get_json() or {})
    read_dto = user_service.activate_user(payload.code)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.get("/activation/resend")  # type: ignore
@inject
def resend_activation(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to resend a new activation code to the user.

    Expects query parameters conforming to ResendActivationCodeSchema.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP 200.
    """
    payload = ResendActivationCodeSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_resend_activation_code(payload)
    read_dto = user_service.resend_activation_code(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.get("/identifier")  # type: ignore
@inject
def get_user_by_identifier(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to retrieve an active user by username or email.

    Expects query parameters conforming to IdentifierSchema.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP 200.
    """
    payload = IdentifierSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_identifier(payload)
    read_dto = user_service.get_by_username_or_email(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.get("/id")  # type: ignore
@inject
def get_user_by_id(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to retrieve a user by ID.

    Expects query parameters conforming to UserIDSchema.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP 200.
    """
    payload = UserIDSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_user_id(payload)
    read_dto = user_service.get_by_id(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.post("/auth/check")  # type: ignore
@inject
def verify_login(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to verify user credentials (login).

    Expects a JSON payload conforming to LoginSchema.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP 200.
    """
    payload = LoginSchema.model_validate(request.get_json() or {})
    dto = to_dto_login(payload)
    read_dto = user_service.verify_credentials(dto)
    return jsonify(to_schema_user(read_dto).model_dump(mode="json")), 200


@users_bp.post("/password/forgot")  # type: ignore
@inject
def forgot_password(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to request a password reset.

    Expects a JSON payload conforming to ForgotPasswordSchema.

    Returns:
        JSON response with a message and HTTP 200.
    """
    payload = ForgotPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_forgot_password(payload)
    user_service.forgot_password(dto)
    return jsonify({"message": "If the email exist, a reset link has been sent."}), 200


@users_bp.post("/password/reset")  # type: ignore
@inject
def reset_password(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to reset a user's password using a reset token.

    Expects a JSON payload conforming to ResetPasswordSchema.

    Returns:
        JSON response with a message and HTTP 200.
    """
    payload = ResetPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_reset_password(payload)
    user_service.reset_password(dto)
    return jsonify({"message": "Password has been reset successfully."}), 200


@users_bp.patch("/mfa/enable")  # type: ignore
@inject
def enable_mfa(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to enable MFA for a user.

    Expects a JSON payload conforming to EnableMfaSchema.

    Returns:
        JSON response with MFA setup data (MfaSetupSchema) and HTTP 200.
    """
    payload = EnableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_mfa_enable(payload)
    result = user_service.enable_mfa(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200


@users_bp.patch("/mfa/disable")  # type: ignore
@inject
def disable_mfa(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to disable MFA for a user.

    Expects a JSON payload conforming to DisableMfaSchema.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP 200.
    """
    payload = DisableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_mfa_disable(payload)
    result = user_service.disable_mfa(dto)
    return jsonify(to_schema_user(result).model_dump(mode="json")), 200


@users_bp.get("/mfa/qr")  # type: ignore
@inject
def get_mfa_qrcode(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to retrieve a user's MFA QR code.

    Expects query parameters conforming to UserIDSchema.

    Returns:
        JSON response with MFA setup data (MfaSetupSchema) and HTTP 200.
    """
    payload = UserIDSchema.model_validate(request.args.to_dict(flat=True))
    dto = to_dto_get_mfa_qrcode(payload)
    result = user_service.get_mfa_qrcode(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200


@users_bp.delete("/id")  # type: ignore
@inject
def delete_by_id(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to delete a user by ID.

    Expects query parameters conforming to DeleteUserByIdSchema.

    Returns:
        Empty response with HTTP 204.
    """
    payload = DeleteUserByIdSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_delete_user_by_id(payload)
    user_service.delete_by_id(dto)
    return "", 204


@users_bp.delete("/identifier")  # type: ignore
@inject
def delete_by_identifier(user_service: UserService = Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Endpoint to delete a user by username or email.

    Expects query parameters conforming to DeleteUserByIdentifierSchema.

    Returns:
        Empty response with HTTP 204.
    """
    payload = DeleteUserByIdentifierSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_delete_user_by_identifier(payload)
    user_service.delete_by_identifier(dto)
    return "", 204


@users_bp.get("/health")  # type: ignore
def health() -> ResponseReturnValue:
    """
    Health check endpoint.

    Returns:
        JSON response with the status of the service and database.
        HTTP 200 if healthy, 503 if database is down.
    """
    health_status = {
        "status": "ok",
        "database": "ok",
        "user_service": "ok"
    }
    status_code = 200

    if not check_db_connection():
        health_status["database"] = "down"
        health_status["status"] = "error"
        status_code = 503

    return jsonify(health_status), status_code


def check_db_connection() -> bool:
    """
    Checks MongoDB connection.

    Returns:
        True if the connection is successful, False otherwise.
    """
    try:
        db.connection.get_connection().admin.command("ping")
        return True
    except Exception:
        return False