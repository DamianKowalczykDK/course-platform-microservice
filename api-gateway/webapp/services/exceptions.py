import httpx

class ApiException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_code: str = "error", details: list | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or []

class ValidationException(ApiException):
    def __init__(self, message: str = "Validation failed", details: list | None = None):
        super().__init__(message, status_code=400, error_code="validation_error", details=details)

class NotFoundException(ApiException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="not_found")

class ConflictException(ApiException):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message, status_code=409, error_code='conflict')

class ServerException(ApiException):
    def __init__(self, message: str = "Server error") -> None:
        super().__init__(message, status_code=500, error_code="server_error")


def extract_message(resp: httpx.Response) -> tuple[str, str, list]:
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
    message, error_code, details = extract_message(resp)

    if resp.status_code == 404:
        raise NotFoundException(not_found_message or message)
    if 400 <= resp.status_code < 500:
        if error_code == "validation_error":
            raise ValidationException(message=message, details=details)
        raise ValidationException(message=message)
    if resp.status_code >= 500:
        raise ServerException(message)
