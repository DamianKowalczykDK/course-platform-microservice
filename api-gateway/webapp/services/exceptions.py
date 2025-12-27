import httpx

class ApiException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_code: str = "error"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class ValidationException(ApiException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=400, error_code="validation_error")

class NotFoundException(ApiException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="not_found")

class ConflictException(ApiException):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message, status_code=409, error_code='conflict')

class ServerException(ApiException):
    def __init__(self, message: str = "Server error") -> None:
        super().__init__(message, status_code=500, error_code="server_error")


def extract_message(resp: httpx.Response) -> str:
    try:
        data = resp.json()
        return data.get("message", resp.text)
    except ValueError:
        return resp.text

def raise_for_status(resp: httpx.Response, not_found_message: str | None = None) -> None:
    if resp.status_code == 404:
        raise NotFoundException(not_found_message or extract_message(resp))
    if 400 <= resp.status_code < 500:
        raise ValidationException(extract_message(resp))
    if resp.status_code >= 500:
        raise ServerException(extract_message(resp))
