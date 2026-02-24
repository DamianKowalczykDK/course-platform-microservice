from flask_mail import Message
from flask import current_app
from webapp.extensions import mail

class EmailService:
    """
    Service to send emails via Flask-Mail.
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
        Send an email to a recipient.

        Args:
            to (str): Recipient email address.
            subject (str): Email subject.
            body (str | None): Plain text body of the email.
            html (str | None): HTML body of the email.
            sender (str | None): Sender email. Uses default sender if None.

        Returns:
            None
        """
        msg = Message(
            subject=subject,
            recipients=[to],
            html=html,
            body=body,
            sender=sender or current_app.config["MAIL_DEFAULT_SENDER"],
        )
        mail.send(msg)