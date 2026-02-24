from typing import Callable
from flask import jsonify
from flask.typing import ResponseReturnValue
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from webapp.container import Container
from webapp.services.users.dtos import UserIdDTO
from webapp.services.users.services import UserService


def role_required(*roles: str) -> Callable[[Callable[..., ResponseReturnValue]], Callable[..., ResponseReturnValue]]:
    """
    Decorator factory to restrict access to users with specific roles.

    Args:
        *roles (str): Allowed roles. If empty, allows any authenticated user.

    Returns:
        Callable: Decorator function that enforces role-based access.
    """
    def wrapper(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
        @wraps(func)
        def decorated(*args, **kwargs) -> ResponseReturnValue:
            verify_jwt_in_request()
            user_id = get_jwt_identity()

            container = Container()
            user_service: UserService = container.user_service()

            dto = UserIdDTO(user_id=user_id)
            user = user_service.get_user_by_id(dto)

            if roles and user.role not in roles:
                return jsonify({"Message": "Forbidden"}), 403

            return func(*args, **kwargs)
        return decorated
    return wrapper


def admin_required(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
    """
    Decorator to allow access only to users with the 'admin' role.

    Args:
        func (Callable): Endpoint function.

    Returns:
        Callable: Wrapped function with admin role check.
    """
    return role_required("admin")(func)


def user_required(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
    """
    Decorator to allow access only to users with the 'user' role.

    Args:
        func (Callable): Endpoint function.

    Returns:
        Callable: Wrapped function with user role check.
    """
    return role_required("user")(func)


def any_authenticated(func: Callable[..., ResponseReturnValue]) -> Callable[..., ResponseReturnValue]:
    """
    Decorator to allow access to any authenticated user, regardless of role.

    Args:
        func (Callable): Endpoint function.

    Returns:
        Callable: Wrapped function that requires authentication.
    """
    return role_required()(func)