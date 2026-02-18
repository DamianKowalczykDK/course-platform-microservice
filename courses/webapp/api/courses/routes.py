from dependency_injector.wiring import Provide, inject
from flask.typing import ResponseReturnValue
from flask import request, jsonify
from webapp.container import Container
from webapp.services.courses.services import CourseService
from . import course_bp
from .mappers import to_dto_create, to_schema_course, to_dto_course_id, to_dto_course_name, to_dto_update_course
from .schemas import CreateCourseSchema, CourseIdSchema, CourseNameSchema, UpdateCourseSchema
from webapp.extensions import db


@course_bp.post('/')
@inject
def create_course(course_service: CourseService=Provide[Container.courses_service]) -> ResponseReturnValue:
    payload = CreateCourseSchema.model_validate(request.get_json() or {})
    dto = to_dto_create(payload)
    read_dto =course_service.create_course(dto)
    return jsonify(to_schema_course(read_dto).model_dump(mode="json")), 201


@course_bp.get("/<int:course_id>")
@inject
def get_by_id(course_id: int, course_service: CourseService=Provide[Container.courses_service]) -> ResponseReturnValue:
    payload = CourseIdSchema.model_validate({"course_id": course_id})
    dto = to_dto_course_id(payload)
    read_dto = course_service.get_by_id(dto)
    return jsonify(to_schema_course(read_dto).model_dump(mode="json")), 200

@course_bp.get("/")
@inject
def get_by_name(course_service: CourseService=Provide[Container.courses_service]) -> ResponseReturnValue:
    payload = CourseNameSchema.model_validate(request.args.to_dict() or {})
    dto = to_dto_course_name(payload)
    read_dto = course_service.get_by_name(dto)
    return jsonify(to_schema_course(read_dto).model_dump(mode="json")), 200

@course_bp.patch("/<int:course_id>")
@inject
def update_course(course_id: int, course_service: CourseService=Provide[Container.courses_service]) -> ResponseReturnValue:
    payload = UpdateCourseSchema.model_validate(request.get_json() or {})
    dto = to_dto_update_course(course_id, payload)
    read_dto = course_service.update_course(dto)
    return jsonify(to_schema_course(read_dto).model_dump(mode="json")), 200

@course_bp.delete("/<int:course_id>")
@inject
def delete_course_by_id(course_id: int, course_service: CourseService=Provide[Container.courses_service]) -> ResponseReturnValue:
    payload = CourseIdSchema.model_validate({"course_id": course_id})
    dto = to_dto_course_id(payload)
    course_service.delete_by_id(dto)
    return "", 204

@course_bp.get("/health")
def health() -> ResponseReturnValue:
    health_status = {
        "status": "ok",
        "database": "ok",
        "user_service": "ok"
    }
    status_code = 200


    if not check_db_connection():
        health_status["database"] = "down"
        health_status["status"] = "error"
        status_code = 503

    return jsonify(health_status), status_code

from sqlalchemy import text
def check_db_connection() -> bool:
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        return False


