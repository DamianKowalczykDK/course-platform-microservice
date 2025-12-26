from flask import jsonify
from flask.typing import ResponseReturnValue
from webapp.api.auth.decorators import admin_required, user_required, any_authenticated
from .import protected_bp

@protected_bp.get("/admin-only")
@admin_required
def admin_only() -> ResponseReturnValue:
    return jsonify({"Message": "Hello, Administrator!"}), 200

@protected_bp.get("/user-only")
@user_required
def user_only() -> ResponseReturnValue:
    return jsonify({"Message": "Hello, User!"}), 200

@protected_bp.get("/any-authenticated")
@any_authenticated
def any_authenticated_only() -> ResponseReturnValue:
    return jsonify({"Message": "Hello, authenticated user!"}), 200


