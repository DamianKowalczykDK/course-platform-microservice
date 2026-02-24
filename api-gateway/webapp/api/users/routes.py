from webapp.api.auth.decorators import user_required, admin_required
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
    to_dto_mfa_qr,
    to_dto_delete_user_by_id,
    to_dto_delete_user_by_identifier
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
    GetMfaSchema,
    DeleteUserByIdSchema,
    DeleteUserByIdentifierSchema
)
from . import users_bp


@users_bp.post("")
@inject
def create_user(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Create a new user.

    Request Body:
        CreateUserSchema: JSON payload with user details (username, first_name, last_name, email, password, gender, role).

    Returns:
        JSON response with created user data (UserResponseSchema) and HTTP status 201.
    """
    payload = CreateUserSchema.model_validate(request.get_json() or {})
    dto = to_dto_create(payload)
    user = user_service.create_user(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 201


@users_bp.get("/id")
@admin_required
@inject
def get_user_by_id(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Get a user by ID.

    Query Parameters:
        user_id (str): User ID.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP status 200.
    """
    payload = UserIdSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_user_id(payload)
    user = user_service.get_user_by_id(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200


@users_bp.get("/identifier")
@admin_required
@inject
def get_user_by_identifier(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Get a user by username or email.

    Query Parameters:
        identifier (str): Username or email.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP status 200.
    """
    payload = IdentifierSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_identifier(payload)
    user = user_service.get_user_by_identifier(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200


@users_bp.patch("/activation")
@inject
def activate_user(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Activate a user using an activation code.

    Request Body:
        ActivationCodeSchema: JSON payload with activation code.

    Returns:
        JSON response with updated user data (UserResponseSchema) and HTTP status 200.
    """
    payload = ActivationCodeSchema.model_validate(request.get_json() or {})
    dto = to_dto_activate(payload)
    user = user_service.activate_user(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200


@users_bp.get("/activation/resend")
@inject
def resend_activation(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Resend activation code to a user.

    Query Parameters:
        identifier (str): Username or email.

    Returns:
        JSON response with user data (UserResponseSchema) and HTTP status 200.
    """
    payload = ResendActivationCodeSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_resend_activation_code(payload)
    user = user_service.resend_activation_code(dto)
    return jsonify(to_schema_user(user).model_dump(mode="json")), 200


@users_bp.post("/password/forgot")
@inject
def forgot_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Request a password reset link for a user.

    Request Body:
        ForgotPasswordSchema: JSON payload with user identifier.

    Returns:
        JSON message confirming email was sent and HTTP status 200.
    """
    payload = ForgotPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_forgot_password(payload)
    user_service.forgot_password(dto)
    return jsonify({"message": "If the email exists, a reset link has been sent."}), 200


@users_bp.post("/password/reset")
@inject
def reset_password(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Reset a user's password using a reset token.

    Request Body:
        ResetPasswordSchema: JSON payload with token and new password.

    Returns:
        JSON message confirming password reset and HTTP status 200.
    """
    payload = ResetPasswordSchema.model_validate(request.get_json() or {})
    dto = to_dto_reset_password(payload)
    user_service.reset_password(dto)
    return jsonify({"message": "Password has been reset successfully."}), 200


@users_bp.patch("/mfa/enable")
@user_required
@inject
def enable_mfa(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Enable multi-factor authentication (MFA) for a user.

    Request Body:
        EnableMfaSchema: JSON payload with user ID.

    Returns:
        JSON response with MFA setup data (MfaSetupSchema) and HTTP status 200.
    """
    payload = EnableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_enable_mfa(payload)
    result = user_service.enable_mfa(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200


@users_bp.patch("/mfa/disable")
@user_required
@inject
def disable_mfa(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Disable MFA for a user.

    Request Body:
        DisableMfaSchema: JSON payload with user ID.

    Returns:
        JSON response with updated user data (UserResponseSchema) and HTTP status 200.
    """
    payload = DisableMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_disable_mfa(payload)
    result = user_service.disable_mfa(dto)
    return jsonify(to_schema_user(result).model_dump(mode="json")), 200


@users_bp.get("/mfa/qr")
@inject
def get_mfa_qr_code(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Retrieve MFA QR code for a user.

    Query Parameters:
        user_id (str): User ID.

    Returns:
        JSON response with MFA setup data (MfaSetupSchema) and HTTP status 200.
    """
    payload = GetMfaSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_mfa_qr(payload)
    result = user_service.get_mfa_qr_code(dto)
    return jsonify(to_schema_mfa_setup(result).model_dump(mode="json")), 200

@users_bp.delete("/id")
@admin_required
@inject
def delete_user_by_id(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Delete a user by ID. Admin access required.

    Query Parameters:
        user_id (str): User ID.

    Returns:
        Empty response with HTTP status 204 on success.
    """
    payload = DeleteUserByIdSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_delete_user_by_id(payload)
    user_service.delete_user_by_id(dto)
    return "", 204

@users_bp.delete("/identifier")
@admin_required
@inject
def delete_user_by_identifier(user_service: UserService=Provide[Container.user_service]) -> ResponseReturnValue:
    """
    Delete a user by username or email. Admin access required.

    Query Parameters:
        identifier (str): Username or email.

    Returns:
        Empty response with HTTP status 204 on success.
    """
    payload = DeleteUserByIdentifierSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_delete_user_by_identifier(payload)
    user_service.delete_user_by_identifier(dto)
    return "", 204
