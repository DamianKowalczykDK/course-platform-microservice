from flask import request, jsonify
from flask.typing import ResponseReturnValue
from dependency_injector.wiring import Provide, inject
from webapp.container import Container
from webapp.api.enrolments.schemas import CreateEnrolmentSchema, EnrolmentIdSchema
from webapp.api.enrolments.mappers import to_enrolment_response_schema, to_create_enrolment_dto, to_enrolment_id_dto
from webapp.services.enrolments.services import EnrolmentService
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

@enrolment_bp.get("/<int:enrolment_id>")
@inject
def get_by_id(enrolment_id: int, enrolment_service: EnrolmentService= Provide[Container.enrolment_service]) -> ResponseReturnValue:
    payload = EnrolmentIdSchema.model_validate({"enrolment_id": enrolment_id})
    dto =  to_enrolment_id_dto(payload)
    read_dto = enrolment_service.get_by_id(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 200
