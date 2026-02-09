from dataclasses import dataclass

@dataclass(frozen=True)
class InvoiceDTO:
    client_name: str
    client_email: str
    course_name: str
    price: int