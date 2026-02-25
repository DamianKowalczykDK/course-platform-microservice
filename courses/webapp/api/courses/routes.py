from dependency_injector.wiring import Provide, inject
from flask.typing import ResponseReturnValue
from flask import request, jsonify
from sqlalchemy import text
from webapp.container import Container
from webapp.extensions import db
from webapp.services.courses.services import CourseService
from .mappers import (
    to_dto_create,
    to_schema_course,
    to_dto_course_id,
    to_dto_course_name,
    to_dto_update_course,
    to_courses_list_response_schema
)
from .schemas import (
    CreateCourseSchema,
    CourseIdSchema,
    CourseNameSchema,
    UpdateCourseSchema
)
from . import course_bp


@course_bp.post('/')
@inject
def create_course(course_service: CourseService = Provide[Container.courses_service]) -> ResponseReturnValue:
    """
    Create a new course.

    Validates the incoming JSON payload using CreateCourseSchema,
    converts it to a DTO, creates the course via CourseService,
    and returns the created course as JSON.

    Args:
        course_service (CourseService): Injected course service.

    Returns:
        ResponseReturnValue: JSON response containing created course data, status code 201.
    """
    payload = CreateCourseSchema.model_validate(request.get_json() or {})
    dto = to_dto_create(payload)
    read_dto = course_service.create_course(dto)
    return jsonify(to_schema_course(read_dto).model_dump(mode="json")), 201


@course_bp.get("/<int:course_id>")
@inject
def get_by_id(course_id: int, course_service: CourseService = Provide[Container.courses_service]) -> ResponseReturnValue:
    """
    Retrieve a course by its ID.

    Args:
        course_id (int): ID of the course to retrieve.
        course_service (CourseService): Injected course service.

    Returns:
        ResponseReturnValue: JSON response containing the course data, status code 200.
    """
    payload = CourseIdSchema.model_validate({"course_id": course_id})
    dto = to_dto_course_id(payload)
    read_dto = course_service.get_by_id(dto)
    return jsonify(to_schema_course(read_dto).model_dump(mode="json")), 200


@course_bp.get("/")
@inject
def get_by_name(course_service: CourseService = Provide[Container.courses_service]) -> ResponseReturnValue:
    """
       Retrieve courses by name via query parameter.

       Args:
           course_service (CourseService): Injected service used to fetch courses.

       Returns:
           ResponseReturnValue: JSON response containing a list of courses in the format of
                                CourseResponseListSchema, with HTTP status code 200.
                                Raises NotFoundException if no matching courses are found.
       """
    payload = CourseNameSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_course_name(payload)
    dtos = course_service.get_by_name(dto)
    courses =to_courses_list_response_schema(dtos)
    return jsonify(courses.model_dump(mode="json")), 200



@course_bp.patch("/<int:course_id>")
@inject
def update_course(course_id: int, course_service: CourseService = Provide[Container.courses_service]) -> ResponseReturnValue:
    """
    Update an existing course.

    Validates the incoming JSON payload, converts it to an UpdateCourseDTO,
    updates the course via CourseService, and returns the updated course.

    Args:
        course_id (int): ID of the course to update.
        course_service (CourseService): Injected course service.

    Returns:
        ResponseReturnValue: JSON response containing updated course data, status code 200.
    """
    payload = UpdateCourseSchema.model_validate(request.get_json() or {})
    dto = to_dto_update_course(course_id, payload)
    read_dto = course_service.update_course(dto)
    return jsonify(to_schema_course(read_dto).model_dump(mode="json")), 200


@course_bp.delete("/<int:course_id>")
@inject
def delete_course_by_id(course_id: int, course_service: CourseService = Provide[Container.courses_service]) -> ResponseReturnValue:
    """
    Delete a course by its ID.

    Args:
        course_id (int): ID of the course to delete.
        course_service (CourseService): Injected course service.

    Returns:
        ResponseReturnValue: Empty response with status code 204.
    """
    payload = CourseIdSchema.model_validate({"course_id": course_id})
    dto = to_dto_course_id(payload)
    course_service.delete_by_id(dto)
    return "", 204


@course_bp.get("/health")
def health() -> ResponseReturnValue:
    """
    Health check endpoint for the service.

    Checks the database connection and service status.

    Returns:
        ResponseReturnValue: JSON response indicating health status with appropriate HTTP status code.
    """
    health_status = {
        "status": "ok",
        "database": "ok",
        "course_service": "ok"
    }
    status_code = 200

    if not check_db_connection():
        health_status["database"] = "down"
        health_status["status"] = "error"
        status_code = 503

    return jsonify(health_status), status_code


def check_db_connection() -> bool:
    """
    Check if the database connection is healthy.

    Executes a simple test query to verify connectivity.

    Returns:
        bool: True if the database is reachable, False otherwise.
    """
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception:
        return False