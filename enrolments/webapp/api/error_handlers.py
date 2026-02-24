from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from typing import TypedDict, Sequence
from pydantic import ValidationError
from webapp.services.exceptions import ApiException

"""
This module registers global error handlers for the Flask application.

It handles:
- Custom API exceptions (ApiException)
- Pydantic validation errors
- 404 Not Found errors
- General unhandled exceptions
"""

class ValidationErrorItem(TypedDict):
    """Structure for individual Pydantic validation errors."""
    loc: Sequence[str | int]
    msg: str
    type: str | None

def register_error_handlers(app: Flask) -> None:
    """Register all error handlers on the Flask app."""

    @app.errorhandler(ApiException)
    def handle_api_exception(error: ApiException) -> ResponseReturnValue:
        """Handle custom API exceptions."""
        return jsonify({
            "message": error.message,
            "error": error.error_code,
        }), error.status_code

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error: ValidationError) -> ResponseReturnValue:
        """Handle Pydantic model validation errors."""
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
        """Handle 404 Not Found errors."""
        return jsonify({
            'message': 'The requested resource was not found.',
            'error': 'not_found'
        }), 404

    @app.errorhandler(Exception)
    def handle_error(e: Exception) -> ResponseReturnValue:
        """Handle unexpected internal server errors."""
        app.logger.info(str(e))
        return jsonify({
            'message': 'Unexpected server error.',
            'error': 'internal_error'
        }), 500