class ApiException(Exception):
    """
    Base exception for API errors.

    Attributes:
        message (str): Error message.
        status_code (int): HTTP status code associated with the error.
        error_code (str): Machine-readable error code.
    """
    def __init__(self, message: str, status_code: int = 400, error_code: str = "error"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class ValidationException(ApiException):
    """
    Raised when input validation fails.
    """
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=400, error_code="validation_error")


class NotFoundException(ApiException):
    """
    Raised when a requested resource is not found.
    """
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="not_found")


class ConflictException(ApiException):
    """
    Raised when an operation conflicts with the current state (e.g., duplicate entry).
    """
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message, status_code=409, error_code='conflict')


class ServiceException(ApiException):
    """
    Raised when a generic service-level error occurs.
    """
    def __init__(self, message: str = "Service error") -> None:
        super().__init__(message, status_code=500, error_code="service_error")


class InvoiceCreationException(ApiException):
    """
    Raised when invoice creation fails.
    """
    def __init__(self, message: str = "Service error") -> None:
        super().__init__(message, status_code=422, error_code="service_error")