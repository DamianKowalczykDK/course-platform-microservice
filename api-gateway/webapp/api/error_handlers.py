import traceback
from typing import TypedDict
from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from webapp.services.exceptions import ApiException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiException)
    def handle_api_exception(error: ApiException) -> ResponseReturnValue:
        return jsonify({
            "message": error.message,
            "status": error.error_code,
        }), error.status_code

    @app.errorhandler(404)
    def handle_not_found_error(error: Exception) -> ResponseReturnValue:
        return jsonify({
            "Message": "The requested resource could not be found.",
            "error": "not_found",
           }
        ), 404

    @app.errorhandler(Exception)
    def handle_generic(error: Exception) -> ResponseReturnValue:
        return jsonify({
            "Message": "Unexpected error.",
            "error": "internal_error"
        }), 500

