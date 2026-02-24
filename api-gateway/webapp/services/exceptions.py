import httpx

class ApiException(Exception):
    """
    Base exception for API-related errors.

    Attributes:
        message (str): Error message.
        status_code (int): HTTP status code associated with the error.
        error_code (str): Custom error code.
        details (list): Optional additional error details.
    """
    def __init__(self, message: str, status_code: int = 400, error_code: str = "error", details: list | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or []

class ValidationException(ApiException):
    """
    Exception raised for validation errors (HTTP 400).

    Args:
        message (str): Error message.
        details (list, optional): List of validation error details.
    """
    def __init__(self, message: str = "Validation failed", details: list | None = None):
        super().__init__(message, status_code=400, error_code="validation_error", details=details)

class NotFoundException(ApiException):
    """
    Exception raised when a resource is not found (HTTP 404).

    Args:
        message (str): Error message.
    """
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="not_found")

class ConflictException(ApiException):
    """
    Exception raised when there is a conflict (HTTP 409).

    Args:
        message (str): Error message.
    """
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message, status_code=409, error_code='conflict')

class ServerException(ApiException):
    """
    Exception raised for server errors (HTTP 500).

    Args:
        message (str): Error message.
    """
    def __init__(self, message: str = "Server error") -> None:
        super().__init__(message, status_code=500, error_code="server_error")


def extract_message(resp: httpx.Response) -> tuple[str, str, list]:
    """
    Extract standardized error information from an HTTP response.

    Args:
        resp (httpx.Response): The HTTP response object.

    Returns:
        tuple: A tuple of (message, error_code, details).
    """
    try:
        data = resp.json()
        return (
            data.get("message", resp.text),
            data.get("error", "error"),
            data.get("details", []),
        )
    except ValueError:
        return resp.text, "error", []

def raise_for_status(resp: httpx.Response, not_found_message: str | None = None) -> None:
    """
    Raise an appropriate API exception based on the HTTP response status.

    Args:
        resp (httpx.Response): The HTTP response object.
        not_found_message (str, optional): Custom message for 404 NotFoundException.

    Raises:
        NotFoundException: If the response status is 404.
        ValidationException: If the response indicates a client error (400–499).
        ServerException: If the response indicates a server error (500+).
    """
    message, error_code, details = extract_message(resp)

    if resp.status_code == 404:
        raise NotFoundException(not_found_message or message)
    if 400 <= resp.status_code < 500:
        if error_code == "validation_error":
            raise ValidationException(message=message, details=details)
        raise ValidationException(message=message)
    if resp.status_code >= 500:
        raise ServerException(message)