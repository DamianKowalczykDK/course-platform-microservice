from typing import Generator
from unittest.mock import patch, MagicMock

import pytest
from flask import Flask

from webapp.services.exceptions import InvoiceCreationException
from webapp.services.invoices.services import InvoiceService
from webapp.services.invoices.dtos import InvoiceDTO

@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    app.config["INVOICE_API_TOKEN"] = "http://invoice-service"
    app.config["INVOICE_DOMAIN"] = "invoice-service"
    with app.app_context():
        yield app

@pytest.fixture
def invoice_service() -> InvoiceService:
    return InvoiceService()

def test_create_invoice(app: Flask, invoice_service: InvoiceService) -> None:
    data: InvoiceDTO = InvoiceDTO(
        client_name="Test",
        client_email="test@example.com",
        course_name="test",
        price=100
    )

    with patch("httpx.Client") as mock_client:
        mock_client_instance = mock_client.return_value

        fake_invoice = MagicMock()
        mock_client_instance.post = fake_invoice

        invoice_service.create_invoice(data)
        mock_client.assert_called()

def test_create_invoice_invoice_creation_exception(app: Flask, invoice_service: InvoiceService) -> None:
    data: InvoiceDTO = InvoiceDTO(
        client_name="Test",
        client_email="test@example.com",
        course_name="test",
        price=100
    )

    with patch("httpx.Client") as mock_client:
        mock_client_instance = mock_client.return_value.__enter__.return_value

        fake_response = MagicMock()
        fake_response.status_code = 422
        mock_client_instance.post.return_value = fake_response

        with pytest.raises(InvoiceCreationException, match="Invoice creation failed"):
            invoice_service.create_invoice(data)

        mock_client.assert_called()