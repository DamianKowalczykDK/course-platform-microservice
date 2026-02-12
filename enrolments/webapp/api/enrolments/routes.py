from dependency_injector.wiring import Provide, inject
from flask import request, jsonify
from flask.typing import ResponseReturnValue
from webapp.api.enrolments.mappers import(
    to_enrolment_response_schema,
    to_create_enrolment_dto,
    to_enrolment_id_dto,
    to_enrolment_by_user_dto,
    to_enrolment_delete_dto
)
from webapp.api.enrolments.schemas import (
    CreateEnrolmentSchema,
    EnrolmentIdSchema,
    EnrolmentByUserSchema,
    DeleteEnrolmentSchema
)
from webapp.container import Container
from webapp.services.enrolments.services import EnrolmentService
from webapp.services.exceptions import ApiException
from . import enrolment_bp


@enrolment_bp.post("/")
@inject
def create_enrolment(enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = CreateEnrolmentSchema.model_validate(request.get_json() or {})
    dto = to_create_enrolment_dto(payload)
    read_dto = enrolment_service.create_enrolment_for_user(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 201

@enrolment_bp.patch("/paid")
@inject
def set_paid(enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = EnrolmentIdSchema.model_validate(request.get_json() or {})
    dto = to_enrolment_id_dto(payload)
    read_dto = enrolment_service.set_paid(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 200

@enrolment_bp.patch("/expired")
@inject
def expired_courses(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    updated_enrolments = enrolment_service.expired_courses()
    return jsonify([to_enrolment_response_schema(e).model_dump(mode="json") for e in updated_enrolments]), 200

@enrolment_bp.get("/<int:enrolment_id>")
@inject
def get_by_id(enrolment_id: int, enrolment_service: EnrolmentService= Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = EnrolmentIdSchema.model_validate({"enrolment_id": enrolment_id})
    dto =  to_enrolment_id_dto(payload)
    read_dto = enrolment_service.get_by_id(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 200

@enrolment_bp.get("/<int:enrolment_id>/details")
@inject
def get_by_id_and_user(enrolment_id: int, enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    user_id = request.args.get("user_id")
    if not user_id:
        raise ApiException(
            message="Missing required query parameter 'user_id'",
            status_code=400,
            error_code="missing_user_id"
        )
    payload = EnrolmentByUserSchema(enrolment_id=enrolment_id, user_id=user_id)
    dto = to_enrolment_by_user_dto(payload)
    read_dto = enrolment_service.get_by_id_and_user(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 200


@enrolment_bp.delete("/<int:enrolment_id>")
@inject
def delete_by_id(enrolment_id: int, enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = DeleteEnrolmentSchema.model_validate({"enrolment_id": enrolment_id})
    dto = to_enrolment_delete_dto(payload)
    enrolment_service.delete_by_id(dto)
    return jsonify(""), 204

