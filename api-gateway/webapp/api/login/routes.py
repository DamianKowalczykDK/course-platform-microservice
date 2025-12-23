from typing import cast

from flask import request, jsonify
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import Provide, inject
from webapp.container import Container
from webapp.api.login.mappers import to_dto_login, to_schema_token_pair, to_dto_verify_mfa
from webapp.api.login.schemas import LoginSchema, VerifyMfaSchema
from webapp.services.auth.services import AuthService
from .import login_bp
from ...services.auth.dtos import TokenPairDTO


@login_bp.post("")
@inject
def login(auth_service: AuthService=Provide[Container.auth_service]) -> ResponseReturnValue:
    payload = LoginSchema.model_validate(request.get_json() or {})
    dto = to_dto_login(payload)
    result = auth_service.login(dto)

    if isinstance(result, dict) and result.get("mfa_required"):
        return jsonify(result), 200

    token_pair_dto: TokenPairDTO = cast(TokenPairDTO, result)
    return jsonify(to_schema_token_pair(token_pair_dto).model_dump(mode="json")), 200

@login_bp.post("/verify-mfa")
@inject
def veryfi_mfa(auth_service: AuthService=Provide[Container.auth_service]) -> ResponseReturnValue:
    payload = VerifyMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_verify_mfa(payload)
    tokens = auth_service.verify_mfa(dto)
    return jsonify(to_schema_token_pair(tokens).model_dump(mode="json")), 200

