from webapp.services.exceptions import ApiException
from flask.typing import ResponseReturnValue
from typing import TypedDict, Sequence
from pydantic import ValidationError
from flask import Flask, jsonify

class ValidationErrorItem(TypedDict):
    """
    TypedDict representing a single validation error item from Pydantic.
    """
    loc: Sequence[str | int]
    msg: str
    type: str | None

def register_error_handlers(app: Flask) -> None:
    """
    Registers error handlers on the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.errorhandler(ApiException)
    def handle_api_exception(error: ApiException) -> ResponseReturnValue:
        """
        Handles custom API exceptions and returns JSON response.

        Args:
            error (ApiException): The raised API exception.

        Returns:
            ResponseReturnValue: JSON response with message and HTTP status code.
        """
        return jsonify({"message": error.message, "error": error.error_code}), error.status_code

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error: ValidationError) -> ResponseReturnValue:
        """
        Handles Pydantic validation errors and returns JSON response with details.

        Args:
            error (ValidationError): The raised Pydantic validation error.

        Returns:
            ResponseReturnValue: JSON response with validation details and HTTP 400.
        """
        errors: list[ValidationErrorItem] = []
        for err in error.errors():
            errors.append({
                "loc": err.get("loc", []),
                "msg": str(err.get("msg")),
                "type": err.get("type"),
            })

        return jsonify({
            "message": "Validation failed",
            "error": "validation_error",
            "details": errors
        }), 400

    @app.errorhandler(404)
    def handle_not_found_error(_: Exception) -> ResponseReturnValue:
        """
        Handles 404 Not Found errors and returns JSON response.

        Args:
            _: The exception instance (ignored).

        Returns:
            ResponseReturnValue: JSON response with HTTP 404 status.
        """
        return jsonify({"message": "The requested resource could not be found"}), 404

    @app.errorhandler(Exception)
    def handle_error(_: Exception) -> ResponseReturnValue:
        """
        Handles uncaught exceptions and returns JSON response.

        Args:
            _: The exception instance (ignored).

        Returns:
            ResponseReturnValue: JSON response with HTTP 500 status.
        """
        return jsonify({"message": "Unexpected error", "error": "internal_error"}), 500