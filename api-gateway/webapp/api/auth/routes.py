from typing import cast
from flask import request, jsonify, Response
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import Provide, inject
from flask_jwt_extended import set_refresh_cookies, jwt_required, unset_jwt_cookies, get_jwt_identity
from webapp.container import Container
from webapp.api.auth.mappers import to_dto_login, to_dto_verify_mfa, to_schema_access_token
from webapp.api.auth.schemas import LoginSchema, VerifyMfaSchema
from webapp.services.auth.services import AuthService
from webapp.extensions import limiter
from webapp.services.auth.dtos import TokenPairDTO, LoginMfaRequiredDTO
from .import auth_bp


@auth_bp.post("/login")
@limiter.limit("2/minute")
@inject
def login(auth_service: AuthService=Provide[Container.auth_service]) -> ResponseReturnValue:
    payload = LoginSchema.model_validate(request.get_json() or {})
    dto = to_dto_login(payload)
    result = auth_service.login(dto)

    if isinstance(result, LoginMfaRequiredDTO) and result.mfa_required:
        return jsonify(result), 200

    tokens_pair_dto: TokenPairDTO = cast(TokenPairDTO, result)
    response: Response = jsonify(to_schema_access_token(tokens_pair_dto).model_dump(mode="json"))
    set_refresh_cookies(response, tokens_pair_dto.refresh_token)
    return response

@auth_bp.post("/mfa/verify")
@inject
def veryfi_mfa(auth_service: AuthService=Provide[Container.auth_service]) -> ResponseReturnValue:
    payload = VerifyMfaSchema.model_validate(request.get_json() or {})
    dto = to_dto_verify_mfa(payload)
    token_pair_dto = auth_service.verify_mfa(dto)

    response: Response = jsonify(to_schema_access_token(token_pair_dto).model_dump(mode="json"))
    set_refresh_cookies(response, token_pair_dto.refresh_token)

    return response

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
@inject
def refresh_token(auth_service: AuthService=Provide[Container.auth_service]) -> ResponseReturnValue:
    identity = get_jwt_identity()
    tokens_pair_dto = auth_service.generate_token(identity)

    response: Response = jsonify(to_schema_access_token(tokens_pair_dto).model_dump(mode="json"))
    set_refresh_cookies(response, tokens_pair_dto.refresh_token)

    return response

@auth_bp.post("/logout")
def logout() -> ResponseReturnValue:
    response: Response = jsonify({"Message": "Logged out"})
    unset_jwt_cookies(response)
    return response
