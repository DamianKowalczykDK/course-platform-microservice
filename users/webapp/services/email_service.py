from flask_mail import Message
from flask import current_app
from webapp.extensions import mail

class EmailService:

    def send_email(
            self,
            to: str,
            subject: str,
            body: str | None = None,
            html: str | None = None,
            sender: str | None = None,
    ) -> None:
        msg = Message(
            subject=subject,
            recipients=[to],
            body=body,
            html=html,
            sender=sender or current_app.config["MAIL_DEFAULT_SENDER"],
        )
        mail.send(msg)
