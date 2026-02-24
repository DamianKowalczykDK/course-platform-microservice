from flask import Flask, jsonify
from flask.typing import ResponseReturnValue
from typing import TypedDict, Sequence
from pydantic import ValidationError
from webapp.services.exceptions import ApiException

class ValidationErrorItem(TypedDict):
    """
    TypedDict representing a single Pydantic validation error item.

    Attributes:
        loc (Sequence[str | int]): Location of the validation error (field path).
        msg (str): Human-readable error message.
        type (str | None): Optional type code for the validation error.
    """
    loc: Sequence[str | int]
    msg: str
    type: str | None


def register_error_handlers(app: Flask) -> None:
    """
    Register global error handlers for the Flask application.

    This function sets up handlers for:
    - ApiException (custom application exceptions)
    - Pydantic ValidationError
    - 404 Not Found errors
    - All other unexpected exceptions

    Args:
        app (Flask): The Flask application instance.
    """

    @app.errorhandler(ApiException)
    def handle_api_exception(error: ApiException) -> ResponseReturnValue:
        """
        Handle custom ApiException errors.

        Returns a JSON response with the message, error code, and status code.

        Args:
            error (ApiException): The raised API exception.

        Returns:
            ResponseReturnValue: Flask JSON response with status code.
        """
        return jsonify({
            "message": error.message,
            "error": error.error_code,
        }), error.status_code

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation_error(error: ValidationError) -> ResponseReturnValue:
        """
        Handle Pydantic validation errors.

        Converts Pydantic validation errors into a structured JSON response.

        Args:
            error (ValidationError): The raised Pydantic validation error.

        Returns:
            ResponseReturnValue: Flask JSON response with status code 400.
        """
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
        """
        Handle 404 Not Found errors.

        Returns a JSON response indicating that the requested resource
        was not found.

        Args:
            _ (Exception): The raised exception (ignored).

        Returns:
            ResponseReturnValue: Flask JSON response with status code 404.
        """
        return jsonify({
            'message': 'The requested resource was not found.',
            'error': 'not_found'
        }), 404

    @app.errorhandler(Exception)
    def handle_error(e: Exception) -> ResponseReturnValue:
        """
        Handle unexpected server errors.

        Logs the exception and returns a generic JSON response.

        Args:
            e (Exception): The raised exception.

        Returns:
            ResponseReturnValue: Flask JSON response with status code 500.
        """
        app.logger.info(str(e))
        return jsonify({
            'message': 'Unexpected server error.',
            'error': 'internal_error'
        }), 500