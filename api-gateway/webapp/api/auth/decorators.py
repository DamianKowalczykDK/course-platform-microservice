from typing import Callable

from flask import jsonify
from flask.typing import ResponseReturnValue
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from webapp.container import Container
from webapp.services.users.dtos import UserIdDTO


def role_required(*roles: str) -> Callable[[Callable[..., ResponseReturnValue]], Callable[..., ResponseReturnValue]]:
    def wrapper(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
        @wraps(func)
        def decorated(*args, **kwargs) -> ResponseReturnValue:
            verify_jwt_in_request()
            user_id = get_jwt_identity()

            container = Container()
            user_service = container.user_service()

            dto = UserIdDTO(user_id=user_id)
            user = user_service.get_user_by_id(dto)

            if roles and user.role not in roles:
                return jsonify({"Message": "Forbidden"}), 403

            return func(*args, **kwargs)
        return decorated
    return wrapper


def admin_required(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
    return role_required("admin")(func)

def user_required(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
    return role_required("user")(func)

def any_authenticated(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
    return role_required()(func)

