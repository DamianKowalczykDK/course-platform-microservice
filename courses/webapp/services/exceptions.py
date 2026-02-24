class ApiException(Exception):
    """
    Base exception class for application-level API errors.

    Stores an error message, HTTP status code, and a machine-readable
    error code that can be returned in API responses.
    """

    def __init__(self, message: str, status_code: int = 400, error_code: str = "error"):
        """
        Initialize the API exception.

        Args:
            message (str): Human-readable error message.
            status_code (int, optional): HTTP status code associated with the error.
            error_code (str, optional): Machine-readable error identifier.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class ValidationException(ApiException):
    """
    Exception raised when input validation fails.
    """

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=400, error_code="validation_error")


class NotFoundException(ApiException):
    """
    Exception raised when a requested resource is not found.
    """

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="not_found")


class ConflictException(ApiException):
    """
    Exception raised when a resource conflict occurs
    (e.g., attempting to create a duplicate entity).
    """

    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message, status_code=409, error_code='conflict')


class ServerException(ApiException):
    """
    Exception raised when an internal server error occurs.
    """

    def __init__(self, message: str = "Server error") -> None:
        super().__init__(message, status_code=500, error_code="server_error")