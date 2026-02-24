from dependency_injector.wiring import Provide, inject
from flask.typing import ResponseReturnValue
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from webapp.services.enrolments.services import EnrolmentService
from webapp.api.enrolments.schemas import (
    CreateEnrolmentSchema,
    EnrolmentIdSchema,
    EnrolmentByUserSchema,
    DeleteEnrolmentSchema
)
from webapp.api.enrolments.mappers import (
    to_create_enrolment_dto,
    to_enrolment_response_schema,
    to_enrolment_id_dto,
    to_enrolment_by_user_dto,
    to_delete_enrolment_dto,
    to_enrolments_list_response_schema
)
from webapp.api.protected.routes import user_required, admin_required
from webapp.container import Container
from . import enrolment_bp


@enrolment_bp.post("")
@user_required
@inject
def create_enrolment_for_user(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Create a new enrolment for the currently authenticated user.

    Request JSON:
        {
            "course_id": int
        }

    Returns:
        201 Created with EnrolmentResponseSchema

    Permissions:
        User must be authenticated.
    """
    payload = CreateEnrolmentSchema.model_validate(request.get_json() or {})
    user_id = get_jwt_identity()
    dto = to_create_enrolment_dto(payload, user_id)
    enrolment = enrolment_service.create_enrolment_for_user(dto)
    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 201


@enrolment_bp.patch("/paid")
@user_required
@inject
def set_paid(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Mark a specific enrolment as paid.

    Request JSON:
        {
            "enrolment_id": int
        }

    Returns:
        200 OK with updated EnrolmentResponseSchema

    Permissions:
        User must be authenticated.
    """
    payload = EnrolmentIdSchema.model_validate(request.get_json() or {})
    dto = to_enrolment_id_dto(payload)
    enrolment = enrolment_service.set_paid(dto)
    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 200


@enrolment_bp.patch("/expired")
@admin_required
@inject
def expired_courses(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Automatically mark all expired enrolments as completed.

    Returns:
        200 OK with EnrolmentsListResponseSchema of updated enrolments

    Permissions:
        Admin only.
    """
    dtos = enrolment_service.expired_courses()
    enrolments = to_enrolments_list_response_schema(dtos)
    return jsonify(enrolments.model_dump(mode="json")), 200


@enrolment_bp.get("/<int:enrolment_id>")
@admin_required
@inject
def get_by_id(enrolment_id: int, enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Get a specific enrolment by its ID.

    Path Parameters:
        enrolment_id (int): ID of the enrolment to retrieve.

    Returns:
        200 OK with EnrolmentResponseSchema

    Permissions:
        Admin only.
    """
    payload = EnrolmentIdSchema(enrolment_id=enrolment_id)
    dto = to_enrolment_id_dto(payload)
    enrolment = enrolment_service.get_by_id(dto)
    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 200


@enrolment_bp.get("/<int:enrolment_id>/details")
@user_required
@inject
def get_by_id_and_user(enrolment_id: int, enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Get a specific enrolment by its ID, but only if it belongs to the authenticated user.

    Path Parameters:
        enrolment_id (int): ID of the enrolment to retrieve.

    Returns:
        200 OK with EnrolmentResponseSchema

    Permissions:
        User must be authenticated.
    """
    user_id = get_jwt_identity()
    payload = EnrolmentByUserSchema(enrolment_id=enrolment_id)
    dto = to_enrolment_by_user_dto(payload, user_id)
    enrolment = enrolment_service.get_by_id_and_user(dto)
    return jsonify(to_enrolment_response_schema(enrolment).model_dump(mode="json")), 200


@enrolment_bp.get("/active")
@admin_required
@inject
def get_active(enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Retrieve all active enrolments.

    Returns:
        200 OK with EnrolmentsListResponseSchema

    Permissions:
        Admin only.
    """
    dtos = enrolment_service.get_active()
    enrolments = to_enrolments_list_response_schema(dtos)
    return jsonify(enrolments.model_dump(mode="json")), 200


@enrolment_bp.delete("/<int:enrolment_id>")
@admin_required
@inject
def delete_by_id(enrolment_id: int, enrolment_service: EnrolmentService=Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Delete a specific enrolment by ID.

    Path Parameters:
        enrolment_id (int): ID of the enrolment to delete.

    Returns:
        204 No Content

    Permissions:
        Admin only.
    """
    payload = DeleteEnrolmentSchema(enrolment_id=enrolment_id)
    dto = to_delete_enrolment_dto(payload)
    enrolment_service.delete_by_id(dto)
    return "", 204