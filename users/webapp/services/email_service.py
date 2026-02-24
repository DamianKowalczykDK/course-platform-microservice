from flask_mail import Message
from flask import current_app
from webapp.extensions import mail

class EmailService:
    """
    Service for sending emails using Flask-Mail.

    Provides a simple interface to send plain text or HTML emails
    with optional custom sender.
    """

    def send_email(
            self,
            to: str,
            subject: str,
            body: str | None = None,
            html: str | None = None,
            sender: str | None = None,
    ) -> None:
        """
        Sends an email to a specified recipient.

        Args:
            to (str): Recipient email address.
            subject (str): Subject of the email.
            body (str | None): Plain text body of the email. Defaults to None.
            html (str | None): HTML body of the email. Defaults to None.
            sender (str | None): Sender email address. Defaults to
                MAIL_DEFAULT_SENDER from Flask app config if not provided.
        """
        msg = Message(
            subject=subject,
            recipients=[to],
            body=body,
            html=html,
            sender=sender or current_app.config["MAIL_DEFAULT_SENDER"],
        )
        mail.send(msg)