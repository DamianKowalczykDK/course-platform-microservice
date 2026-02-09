from urllib.parse import quote_plus
from dotenv import load_dotenv
from logging.config import dictConfig
from flask import Flask
import os

load_dotenv()

class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', "default secret key")
    FLASK_ENV:str = os.getenv('FLASK_ENV', "development")
    FlASK_DEBUG: bool = os.getenv('FLASK_DEBUG') in ("1", "true", "True")

    MYSQL_DIALECT: str = os.getenv('MYSQL_ENROLMENT_DIALECT', 'mysql+mysqldb')
    MYSQL_HOST: str = os.getenv('MYSQL_ENROLMENT_HOST', 'mysql-enrolments')
    MYSQL_DATABASE: str = os.getenv('MYSQL_ENROLMENT_DATABASE', 'db_enrolments')
    MYSQL_USER: str = os.getenv('MYSQL_ENROLMENT_USER', '')
    MYSQL_PASSWORD: str = os.getenv('MYSQL_ENROLMENT_PASSWORD', '')
    MYSQL_ROOT_PASSWORD: str = os.getenv('MYSQL_ENROLMENT_ROOT_PASSWORD', '')
    MYSQL_PORT: str = os.getenv('MYSQL_ENROLMENT_PORT', '3308')

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str: # pragma: no cover
        return (
            f"{self.MYSQL_DIALECT}://{self.MYSQL_USER}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )

    MAIL_SERVER: str=os.getenv('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT: int= int(os.getenv('MAIL_PORT', "587"))
    MAIL_USE_TLS: bool=os.getenv('MAIL_USE_TLS', "True") in ("1", "true", "True")
    MAIL_USE_SSL: bool=os.getenv('MAIL_USE_SSL', "False") in ("1", "true", "True")
    MAIL_USERNAME: str=os.getenv('MAIL_USERNAME', "")
    MAIL_PASSWORD: str=os.getenv('MAIL_PASSWORD', "")
    MAIL_DEFAULT_SENDER: str=os.getenv('MAIL_DEFAULT_SENDER', "")

    USERS_SERVICE_URL: str = os.getenv('USERS_SERVICE_URL', "http://localhost:5000/api/users")
    COURSE_SERVICE_URL: str = os.getenv('COURSE_SERVICE_URL', "http://localhost:5000/api/course")

    INVOICE_API_TOKEN: str = os.getenv('INVOICE_API_TOKEN', "")
    INVOICE_DOMAIN: str = os.getenv('INVOICE_DOMAIN', "")

    @staticmethod
    def configure_logging(app: Flask) -> None: # pragma: no cover
        if getattr(app, "_logging_configured", False):
            return
        app._logging_configured = True # type: ignore

        dictConfig({
            "version": 1,
            "formatters": {"default": {"format": "[%(asctime)s] %(levelname)s: %(message)s"}},
            "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
            "root": {"level": "DEBUG", "handlers": ["console"]},
        })

    @classmethod
    def init_app(cls, app: Flask) -> None: # pragma: no cover
        cls.configure_logging(app)
        app.logger.debug("Logger initialized")
        conf = cls()
        app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI

config: dict[str, type[Config]] = {
    "default": Config,
}


