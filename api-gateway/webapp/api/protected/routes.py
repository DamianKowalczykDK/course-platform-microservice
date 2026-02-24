from flask import jsonify
from flask.typing import ResponseReturnValue
from webapp.api.auth.decorators import admin_required, user_required, any_authenticated
from . import protected_bp

@protected_bp.get("/admin-only")
@admin_required
def admin_only() -> ResponseReturnValue:
    """
    Endpoint accessible only to users with the 'admin' role.

    Returns:
        JSON response with a welcome message for administrators.
    """
    return jsonify({"Message": "Hello, Administrator!"}), 200


@protected_bp.get("/user-only")
@user_required
def user_only() -> ResponseReturnValue:
    """
    Endpoint accessible only to users with the 'user' role.

    Returns:
        JSON response with a welcome message for regular users.
    """
    return jsonify({"Message": "Hello, User!"}), 200


@protected_bp.get("/any-authenticated")
@any_authenticated
def any_authenticated_only() -> ResponseReturnValue:
    """
    Endpoint accessible to any authenticated user, regardless of role.

    Returns:
        JSON response with a welcome message for authenticated users.
    """
    return jsonify({"Message": "Hello, authenticated user!"}), 200