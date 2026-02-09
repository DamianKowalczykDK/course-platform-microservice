from webapp.services.invoices.dtos import InvoiceDTO
from flask import  current_app
import datetime
import httpx

class InvoiceService:
    def __init__(self) -> None:
        domain = current_app.config["INVOICE_DOMAIN"]
        self.api_token = current_app.config["INVOICE_API_TOKEN"]
        self.api_url = f"https://{domain}.fakturownia.pl/invoices.json"
        self.headers = {"Content-Type": "application/json"}

    def create_invoice(self, dto: InvoiceDTO) -> str:

        today = datetime.date.today()

        payload = {
            "api_token": self.api_token,
            "invoice": {
                "kind": "vat",
                "sell_date": today.isoformat(),
                "seller_name": "Damian Kowalczyk",
                "buyer_name": dto.client_name,
                "positions": [
                    {"name": dto.course_name, "tax": 23, "total_price_gross": dto.price, "quantity": 1},
                ]
            }
        }

        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )

        response.raise_for_status()
        if response.status_code == 422:
            raise ValueError(f"Invoice could not be created: {response.text}")

        result = response.json()
        invoice_url = result.get("view_url", "N/A")
        return invoice_url
