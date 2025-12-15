from dependency_injector.wiring import inject
from flask import request, jsonify, Blueprint
import httpx
from flask.typing import ResponseReturnValue
from flask_jwt_extended import create_access_token
from dependency_injector.wiring import Provide, inject
from webapp.container import Container
from webapp.api.login.mappers import to_dto_login, to_schema_token_pair
from webapp.api.login.schemas import LoginSchema
from webapp.services.auth.services import AuthService
from .import login_bp


@login_bp.post("")
@inject
def login(auth_service: AuthService=Provide[Container.auth_service]) -> ResponseReturnValue:
    payload = LoginSchema.model_validate(request.get_json() or {})
    dto = to_dto_login(payload)
    token_pair = auth_service.login(dto)

    return jsonify(to_schema_token_pair(token_pair).model_dump(mode="json")), 200
