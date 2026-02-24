class ApiException(Exception):
    """
    Base class for API exceptions.

    Attributes:
        message (str): Human-readable error message.
        status_code (int): HTTP status code associated with the exception.
        error_code (str): Machine-readable error code.
    """

    def __init__(self, message: str, status_code: int = 400, error_code: str = "error"):
        """
        Initializes an ApiException.

        Args:
            message (str): Error message.
            status_code (int): HTTP status code. Defaults to 400.
            error_code (str): Machine-readable error code. Defaults to "error".
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class ValidationException(ApiException):
    """
    Exception raised when a validation error occurs.

    Defaults to status code 400 and error code "validation_error".
    """

    def __init__(self, message: str = "Validation failed"):
        """
        Initializes a ValidationException.

        Args:
            message (str): Optional custom error message. Defaults to "Validation failed".
        """
        super().__init__(message, status_code=400, error_code="validation_error")

class NotFoundException(ApiException):
    """
    Exception raised when a requested resource is not found.

    Defaults to status code 404 and error code "not_found".
    """

    def __init__(self, message: str = "Resource not found"):
        """
        Initializes a NotFoundException.

        Args:
            message (str): Optional custom error message. Defaults to "Resource not found".
        """
        super().__init__(message, status_code=404, error_code="not_found")

class ConflictException(ApiException):
    """
    Exception raised when a conflict occurs (e.g., duplicate resource).

    Defaults to status code 409 and error code "conflict".
    """

    def __init__(self, message: str = "Conflict") -> None:
        """
        Initializes a ConflictException.

        Args:
            message (str): Optional custom error message. Defaults to "Conflict".
        """
        super().__init__(message, status_code=409, error_code='conflict')

class ServerException(ApiException):
    """
    Exception raised for internal server errors.

    Defaults to status code 500 and error code "server_error".
    """

    def __init__(self, message: str = "Server error") -> None:
        """
        Initializes a ServerException.

        Args:
            message (str): Optional custom error message. Defaults to "Server error".
        """
        super().__init__(message, status_code=500, error_code="server_error")