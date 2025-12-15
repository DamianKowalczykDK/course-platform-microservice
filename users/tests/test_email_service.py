from unittest.mock import MagicMock, patch
import pytest
from webapp.services.email_service import EmailService
from flask import Flask

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config["MAIL_DEFAULT_SENDER"] = "default@example.com"
    return app

@pytest.fixture
def email_service() -> EmailService:
    return EmailService()

@patch("webapp.services.email_service.mail")
@patch("webapp.services.email_service.Message")
def test_send_email_uses_mail_and_message(
        mock_message: MagicMock,
        mock_mail: MagicMock,
        email_service: EmailService,
        app: Flask,
) -> None:
    with app.app_context():
        mock_msg_instance = MagicMock()
        mock_message.return_value = mock_msg_instance
        email_service.send_email(
            to="test@example.com",
            subject="test",
            body="test",
            html="<html>test</html>",
        )

        mock_message.assert_called_once_with(
            subject="test",
            body="test",
            html="<html>test</html>",
            recipients=["test@example.com"],
            sender="default@example.com"
        )

        mock_mail.send.assert_called_once_with(mock_msg_instance)

