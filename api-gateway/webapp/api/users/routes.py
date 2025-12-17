from dependency_injector.wiring import Provide, inject
from flask import request, jsonify
from webapp.api.users.mappers import to_dto_create, to_dto_activate, to_schema_user
from webapp.services.users.services import UserService
from webapp.container import Container
from flask.typing import ResponseReturnValue
from .schemas import CreateUserSchema, ActivationCodeSchema
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


