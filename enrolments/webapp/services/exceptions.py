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

class ServiceException(ApiException):
    def __init__(self, message: str = "Service error") -> None:
        super().__init__(message, status_code=500, error_code="service_error")

class InvoiceCreationException(ApiException):
    def __init__(self, message: str = "Service error") -> None:
        super().__init__(message, status_code=422, error_code="service_error")
