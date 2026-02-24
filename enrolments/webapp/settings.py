from urllib.parse import quote_plus
from dotenv import load_dotenv
from logging.config import dictConfig
from flask import Flask
import os

load_dotenv()

class Config:
    """
    Configuration class for the Enrolments microservice.

    Loads configuration from environment variables for:
    - Flask application settings
    - MySQL database connection
    - SQLAlchemy engine options
    - Mail server settings
    - External service URLs
    - Invoice API credentials
    - HTTP timeout
    """

    SECRET_KEY: str = os.getenv('SECRET_KEY', "")
    FLASK_ENV:str = os.getenv('FLASK_ENV', "")
    FlASK_DEBUG: bool = os.getenv('FLASK_DEBUG') in ("1", "true", "True")

    MYSQL_DIALECT: str = os.getenv('MYSQL_ENROLMENT_DIALECT', '')
    MYSQL_HOST: str = os.getenv('MYSQL_ENROLMENT_HOST', '')
    MYSQL_DATABASE: str = os.getenv('MYSQL_ENROLMENT_DATABASE', '')
    MYSQL_USER: str = os.getenv('MYSQL_ENROLMENT_USER', '')
    MYSQL_PASSWORD: str = os.getenv('MYSQL_ENROLMENT_PASSWORD', '')
    MYSQL_ROOT_PASSWORD: str = os.getenv('MYSQL_ENROLMENT_ROOT_PASSWORD', '')
    MYSQL_PORT: str = os.getenv('MYSQL_ENROLMENT_PORT', '')

    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", ""))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", ""))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", ""))
    DB_POOL_PRE_PING: bool = os.getenv("DB_POOL_PRE_PING", "") in ("1", "true", "True")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str: # pragma: no cover
        """
        Constructs the SQLAlchemy database URI using MySQL credentials.
        """
        return (
            f"{self.MYSQL_DIALECT}://{self.MYSQL_USER}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict: # pragma: no cover
        """
        Returns SQLAlchemy engine options including connection pool settings.
        """
        return {
            "pool_size": self.DB_POOL_SIZE,
            "max_overflow": self.DB_MAX_OVERFLOW,
            "pool_pre_ping": self.DB_POOL_PRE_PING,
            "pool_recycle": self.DB_POOL_RECYCLE,
        }

    MAIL_SERVER: str=os.getenv('MAIL_SERVER', "")
    MAIL_PORT: int= int(os.getenv('MAIL_PORT', ""))
    MAIL_USE_TLS: bool=os.getenv('MAIL_USE_TLS', "") in ("1", "true", "True")
    MAIL_USE_SSL: bool=os.getenv('MAIL_USE_SSL', "") in ("1", "true", "True")
    MAIL_USERNAME: str=os.getenv('MAIL_USERNAME', "")
    MAIL_PASSWORD: str=os.getenv('MAIL_PASSWORD', "")
    MAIL_DEFAULT_SENDER: str=os.getenv('MAIL_DEFAULT_SENDER', "")

    USERS_SERVICE_URL: str = os.getenv('USERS_SERVICE_URL', "")
    COURSE_SERVICE_URL: str = os.getenv('COURSE_SERVICE_URL', "")

    INVOICE_API_TOKEN: str = os.getenv('INVOICE_API_TOKEN', "")
    INVOICE_DOMAIN: str = os.getenv('INVOICE_DOMAIN', "")

    HTTP_TIMEOUT: int = int(os.getenv('HTTP_TIMEOUT', ""))

    @staticmethod
    def configure_logging(app: Flask) -> None: # pragma: no cover
        """
        Configures Flask logging using dictConfig.
        Ensures logging is only configured once per app.
        """
        if getattr(app, "_logging_configured", False):
            return
        app._logging_configured = True  # type: ignore

        dictConfig({
            "version": 1,
            "formatters": {"default": {"format": "[%(asctime)s] %(levelname)s: %(message)s"}},
            "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
            "root": {"level": "DEBUG", "handlers": ["console"]},
        })

    @classmethod
    def init_app(cls, app: Flask) -> None: # pragma: no cover
        """
        Initializes the Flask app with database URI and engine options.
        Also configures logging.
        """
        cls.configure_logging(app)
        app.logger.debug("Logger initialized")
        conf = cls()
        app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = conf.SQLALCHEMY_ENGINE_OPTIONS


config: dict[str, type[Config]] = {
    "default": Config,
}