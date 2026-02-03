from dependency_injector.wiring import Provide, inject
from flask import request, jsonify

from webapp.api.courses.schemas import CreateCourseSchema, CourseIdSchema, CourseNameSchema, UpdateCourseSchema
from webapp.services.courses.services import CourseService
from flask.typing import ResponseReturnValue
from webapp.container import Container
from .mappers import to_dto_create, to_schema_course, to_dto_course_id, to_dto_course_name, to_dto_update_course
from . import course_bp


@course_bp.post("")
@inject
def create_course(course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    payload = CreateCourseSchema.model_validate(request.get_json())
    dto = to_dto_create(payload)
    course = course_service.create_course(dto)
    return jsonify(to_schema_course(course).model_dump(mode="json")), 201


@course_bp.get("/<int:course_id>")
@inject
def get_by_id(course_id: int, course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    payload = CourseIdSchema.model_validate({"course_id": course_id})
    dto = to_dto_course_id(payload)
    course = course_service.get_by_id(dto)
    return jsonify(to_schema_course(course).model_dump(mode="json")), 200

@course_bp.get("/")
@inject
def get_by_name(course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    payload = CourseNameSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_course_name(payload)
    course = course_service.get_by_name(dto)
    return jsonify(to_schema_course(course).model_dump(mode="json")), 200

@course_bp.patch("/<int:course_id>")
@inject
def update_course(course_id: int, course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    payload = UpdateCourseSchema.model_validate(request.get_json() or {})
    dto = to_dto_update_course(course_id, payload)
    course = course_service.update_course(dto)
    return jsonify(to_schema_course(course).model_dump(mode="json")), 200

@course_bp.delete("/<int:course_id>")
@inject
def delete_by_id(course_id: int, course_service: CourseService=Provide[Container.course_service]) -> ResponseReturnValue:
    payload = CourseIdSchema.model_validate({"course_id": course_id})
    dto = to_dto_course_id(payload)
    course_service.delete_by_id(dto)
    return "", 204
