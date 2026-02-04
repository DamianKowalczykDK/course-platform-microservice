from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from typing import TypedDict, Sequence
from pydantic import ValidationError
from webapp.services.exceptions import ApiException

class ValidationErrorItem(TypedDict):
    loc: Sequence[str | int]
    msg: str
    type: str | None

def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiException)
    def handle_api_exception(error: ApiException) -> ResponseReturnValue:
        return jsonify({
            "message": error.message,
            "error": error.error_code,
        }), error.status_code

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error: ValidationError) -> ResponseReturnValue:
        errors: list[ValidationErrorItem] = []
        for err in error.errors():
            errors.append({
                'loc': err.get('loc', []),
                'msg': str(err.get('msg')),
                'type': err.get('type')
            })

        return jsonify({
            'message': 'Validation failed',
            'error': 'validation_error',
            'details': errors
        }), 400

    @app.errorhandler(404)
    def handle_not_found_error(_: Exception) -> ResponseReturnValue:
        return jsonify({
            'message': 'The requested resource was not found.',
            'error': 'not_found'
        }), 404

    @app.errorhandler(Exception)
    def handle_error(e: Exception) -> ResponseReturnValue:
        app.logger.info(str(e))
        return jsonify({
            'message': 'Unexpected server error.',
            'error': 'internal_error'
        }), 500