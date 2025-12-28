from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from webapp.services.exceptions import ApiException
from typing import TypedDict

class ApiExceptionResponse(TypedDict, total=False):
    message: str
    error: str
    details: list

def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiException)
    def handle_api_exception(error: ApiException) -> ResponseReturnValue:
        response: ApiExceptionResponse = {
            "message": error.message,
            "error": error.error_code
        }
        if error.details:
            response['details'] = error.details

        return jsonify(response), error.status_code


    @app.errorhandler(404)
    def handle_not_found_error(_: Exception) -> ResponseReturnValue:
        return jsonify({
            "message": "The requested resource could not be found.",
            "error": "not_found",
        }
        ), 404

    @app.errorhandler(Exception)
    def handle_generic(_: Exception) -> ResponseReturnValue:
        return jsonify({
            "message": "Unexpected error.",
            "error": "internal_error"
        }), 500
