from dependency_injector.wiring import Provide, inject
from flask import request, jsonify
from webapp.api.courses.schemas import (
    CreateCourseSchema,
    CourseIdSchema,
    CourseNameSchema,
    UpdateCourseSchema
)
from webapp.api.auth.decorators import admin_required
from webapp.services.courses.services import CourseService
from flask.typing import ResponseReturnValue
from webapp.container import Container
from .mappers import (
    to_dto_create,
    to_schema_course,
    to_dto_course_id,
    to_dto_course_name,
    to_dto_update_course, to_schema_list_course
)
from . import course_bp


@course_bp.post("")
@admin_required
@inject
def create_course(course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    """
    Create a new course (admin only).

    Validates the incoming payload, maps it to DTO, calls the service,
    and returns the created course.
    """
    payload = CreateCourseSchema.model_validate(request.get_json())
    dto = to_dto_create(payload)
    course = course_service.create_course(dto)
    return jsonify(to_schema_course(course).model_dump(mode="json")), 201


@course_bp.get("/<int:course_id>")
@admin_required
@inject
def get_by_id(course_id: int, course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    """
    Get a course by its ID (admin only).
    """
    payload = CourseIdSchema(course_id=course_id)
    dto = to_dto_course_id(payload)
    course = course_service.get_by_id(dto)
    return jsonify(to_schema_course(course).model_dump(mode="json")), 200


@course_bp.get("/")
@admin_required
@inject
def get_by_name(course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    """
      Retrieve courses by name (admin only).

      Query Parameter:
          name (str): Full or partial name of the course to search.

      Returns:
          ResponseReturnValue: JSON response containing a list of courses in the format
                               of CoursesListResponseSchema, with HTTP status code 200.
                               Raises NotFoundException if no matching courses are found.
      """
    payload = CourseNameSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_course_name(payload)
    dtos = course_service.get_by_name(dto)
    courses = to_schema_list_course(dtos)
    return jsonify(courses.model_dump(mode="json")), 200


@course_bp.patch("/<int:course_id>")
@admin_required
@inject
def update_course(course_id: int, course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    """
    Update an existing course (admin only).

    Validates the update payload, maps to DTO, calls the service,
    and returns the updated course.
    """
    payload = UpdateCourseSchema.model_validate(request.get_json() or {})
    dto = to_dto_update_course(course_id, payload)
    course = course_service.update_course(dto)
    return jsonify(to_schema_course(course).model_dump(mode="json")), 200


@course_bp.delete("/<int:course_id>")
@admin_required
@inject
def delete_by_id(course_id: int, course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    """
    Delete a course by its ID (admin only).
    """
    payload = CourseIdSchema(course_id=course_id)
    dto = to_dto_course_id(payload)
    course_service.delete_by_id(dto)
    return "", 204
