from dependency_injector.wiring import Provide, inject
from flask import request, jsonify
from flask.typing import ResponseReturnValue
from webapp.api.enrolments.mappers import (
    to_enrolment_response_schema,
    to_create_enrolment_dto,
    to_enrolment_id_dto,
    to_enrolment_by_user_dto,
    to_enrolment_delete_dto,
    to_enrolments_list_response_schema
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
from webapp.extensions import db
from sqlalchemy import text


@enrolment_bp.post("/")
@inject
def create_enrolment(enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Create a new enrolment for a user.

    Args:
        enrolment_service (EnrolmentService): The service handling enrolment operations.

    Returns:
        ResponseReturnValue: JSON response containing the created enrolment data and HTTP 201 status.
    """
    payload = CreateEnrolmentSchema.model_validate(request.get_json() or {})
    dto = to_create_enrolment_dto(payload)
    read_dto = enrolment_service.create_enrolment_for_user(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 201


@enrolment_bp.patch("/paid")
@inject
def set_paid(enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Mark an enrolment as paid and send invoice email.

    Args:
        enrolment_service (EnrolmentService): The service handling enrolment operations.

    Returns:
        ResponseReturnValue: JSON response containing the updated enrolment and HTTP 200 status.

    Raises:
        ApiException: If the enrolment is already paid or not found.
    """
    payload = EnrolmentIdSchema.model_validate(request.get_json() or {})
    dto = to_enrolment_id_dto(payload)
    read_dto = enrolment_service.set_paid(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 200


@enrolment_bp.patch("/expired")
@inject
def expired_courses(enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Mark expired courses as completed.

    Args:
        enrolment_service (EnrolmentService): The service handling enrolment operations.

    Returns:
        ResponseReturnValue: JSON response containing the list of updated enrolments and HTTP 200 status.
    """
    dtos = enrolment_service.expired_courses()
    enrolments = to_enrolments_list_response_schema(dtos)
    return jsonify(enrolments.model_dump(mode="json")), 200


@enrolment_bp.get("/<int:enrolment_id>")
@inject
def get_by_id(enrolment_id: int, enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Get enrolment details by enrolment ID.

    Args:
        enrolment_id (int): The ID of the enrolment.
        enrolment_service (EnrolmentService): The service handling enrolment operations.

    Returns:
        ResponseReturnValue: JSON response containing the enrolment details and HTTP 200 status.

    Raises:
        ApiException: If the enrolment is not found.
    """
    payload = EnrolmentIdSchema.model_validate({"enrolment_id": enrolment_id})
    dto = to_enrolment_id_dto(payload)
    read_dto = enrolment_service.get_by_id(dto)
    return jsonify(to_enrolment_response_schema(read_dto).model_dump(mode="json")), 200


@enrolment_bp.get("/<int:enrolment_id>/details")
@inject
def get_by_id_and_user(enrolment_id: int, enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Get enrolment details by enrolment ID and user ID.

    Args:
        enrolment_id (int): The ID of the enrolment.
        enrolment_service (EnrolmentService): The service handling enrolment operations.

    Query Parameters:
        user_id (str): The ID of the user.

    Returns:
        ResponseReturnValue: JSON response containing the enrolment details and HTTP 200 status.

    Raises:
        ApiException: If the user_id query parameter is missing or enrolment is not found.
    """
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


@enrolment_bp.get("/active")
@inject
def get_active(enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Get all active enrolments.

    Args:
        enrolment_service (EnrolmentService): The service handling enrolment operations.

    Returns:
        ResponseReturnValue: JSON response containing the list of active enrolments and HTTP 200 status.

    Raises:
        ApiException: If no active enrolments are found.
    """
    dtos = enrolment_service.get_active()
    enrolments = to_enrolments_list_response_schema(dtos)
    return jsonify(enrolments.model_dump(mode="json")), 200


@enrolment_bp.delete("/<int:enrolment_id>")
@inject
def delete_by_id(enrolment_id: int, enrolment_service: EnrolmentService = Provide[Container.enrolment_service]) -> ResponseReturnValue:
    """
    Delete an enrolment by ID.

    Args:
        enrolment_id (int): The ID of the enrolment to delete.
        enrolment_service (EnrolmentService): The service handling enrolment operations.

    Returns:
        ResponseReturnValue: Empty response with HTTP 204 status.

    Raises:
        ApiException: If the enrolment is not found.
    """
    payload = DeleteEnrolmentSchema.model_validate({"enrolment_id": enrolment_id})
    dto = to_enrolment_delete_dto(payload)
    enrolment_service.delete_by_id(dto)
    return jsonify(""), 204


@enrolment_bp.get("/health")
def health() -> ResponseReturnValue:
    """
    Health check endpoint for the enrolment service.

    Returns:
        ResponseReturnValue: JSON response containing the status of the service and database.
    """
    health_status = {
        "status": "ok",
        "database": "ok",
        "enrolment_service": "ok"
    }
    status_code = 200

    if not check_db_connection():
        health_status["database"] = "down"
        health_status["status"] = "error"
        status_code = 503

    return jsonify(health_status), status_code


def check_db_connection() -> bool:
    """
    Check if the database connection is alive.

    Returns:
        bool: True if the database connection is successful, False otherwise.
    """
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception:
        return False