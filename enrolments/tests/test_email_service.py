from unittest.mock import patch, MagicMock

from flask import Flask

from webapp.services.email_service import EmailService
import pytest


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config["MAIL_DEFAULT_SENDER"] = "default@example.com"
    return app

@pytest.fixture
def email_service() -> EmailService:
    return EmailService()

@patch("webapp.services.email_service.Message")
@patch("webapp.services.email_service.mail")
def test_send_email_uses_mail_and_message(
        mock_mail: MagicMock,
        mock_message: MagicMock,
        email_service: EmailService,
        app: Flask,
) -> None:
    with app.app_context():
        mock_msg = MagicMock()
        mock_message.return_value = mock_msg
        email_service.send_email(
            to="test@example.com",
            body="test",
            html="<html>test</html>",
            subject="test",
        )

        mock_message.assert_called_once_with(
            subject="test",
            recipients=["test@example.com"],
            body="test",
            html="<html>test</html>",
            sender="default@example.com"
        )

    mock_mail.send.assert_called_once_with(mock_msg)