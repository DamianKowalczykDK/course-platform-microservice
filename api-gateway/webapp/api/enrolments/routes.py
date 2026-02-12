from dependency_injector.wiring import Provide, inject
from flask.typing import ResponseReturnValue
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from webapp.services.enrolments.services import EnrolmentService
from webapp.api.enrolments.schemas import CreateEnrolmentSchema, EnrolmentIdSchema, EnrolmentByUserSchema
from webapp.api.enrolments.mappers import (
    to_create_enrolment_dto,
    to_enrolment_response_schema,
    to_enrolment_id_dto,
    to_enrolment_by_user_dto
)
from webapp.api.protected.routes import user_required, admin_required
from webapp.container import Container
from . import enrolment_bp


@enrolment_bp.post("")
@user_required
@inject
def create_enrolment_for_user(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = CreateEnrolmentSchema.model_validate(request.get_json() or {})
    user_id = get_jwt_identity()
    dto = to_create_enrolment_dto(payload, user_id)
    enrolment = enrolment_service.create_enrolment_for_user(dto)
    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 201

@enrolment_bp.patch("/paid")
@user_required
@inject
def set_paid(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = EnrolmentIdSchema.model_validate(request.get_json() or {})
    dto = to_enrolment_id_dto(payload)
    enrolment = enrolment_service.set_paid(dto)
    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 200

@enrolment_bp.patch("/expired")
@admin_required
@inject
def expired_courses(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    update_enrolments = enrolment_service.expired_courses()
    return jsonify([to_enrolment_response_schema(e).model_dump(mode="json") for e in update_enrolments]), 200

@enrolment_bp.get("/<int:enrolment_id>")
@admin_required
@inject
def get_by_id(enrolment_id: int, enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = EnrolmentIdSchema(enrolment_id=enrolment_id)
    dto = to_enrolment_id_dto(payload)
    enrolment = enrolment_service.get_by_id(dto)

    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 200

@enrolment_bp.get("/<int:enrolment_id>/details")
@user_required
@inject
def get_by_id_and_user(enrolment_id: int, enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    user_id = get_jwt_identity()
    payload = EnrolmentByUserSchema(enrolment_id=enrolment_id)
    dto = to_enrolment_by_user_dto(payload, user_id)
    enrolment = enrolment_service.get_by_id_and_user(dto)
    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 200

