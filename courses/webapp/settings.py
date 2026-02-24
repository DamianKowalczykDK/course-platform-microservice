from urllib.parse import quote_plus
from dotenv import load_dotenv
from logging.config import dictConfig
from flask import Flask
import os

load_dotenv()


class Config:
    """
    Flask application configuration class.

    Stores application secrets, environment settings, and MySQL database
    connection parameters. Provides methods to build the SQLAlchemy URI
    and configure logging for the Flask app.
    """

    SECRET_KEY: str = os.getenv('SECRET_KEY', "")
    FLASK_ENV: str = os.getenv('FLASK_ENV', "")
    FlASK_DEBUG: bool = os.getenv('FLASK_DEBUG') in ("1", "true", "True")

    MYSQL_DIALECT: str = os.getenv('MYSQL_DIALECT', '')
    MYSQL_HOST: str = os.getenv('MYSQL_HOST', '')
    MYSQL_DATABASE: str = os.getenv('MYSQL_DATABASE', '')
    MYSQL_USER: str = os.getenv('MYSQL_USER', '')
    MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_ROOT_PASSWORD: str = os.getenv('MYSQL_ROOT_PASSWORD', '')
    MYSQL_PORT: str = os.getenv('MYSQL_PORT', '')

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # pragma: no cover
        """
        Construct the SQLAlchemy database URI from environment variables.

        Returns:
            str: Database URI formatted for SQLAlchemy with UTF-8 encoding.
        """
        return (
            f"{self.MYSQL_DIALECT}://{self.MYSQL_USER}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )

    @staticmethod
    def configure_logging(app: Flask) -> None:  # pragma: no cover
        """
        Configure logging for the Flask application.

        Ensures logging is configured only once per app instance.

        Args:
            app (Flask): The Flask application instance.
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
    def init_app(cls, app: Flask) -> None:  # pragma: no cover
        """
        Initialize the Flask app with configuration and logging.

        Args:
            app (Flask): The Flask application instance.
        """
        cls.configure_logging(app)
        app.logger.debug("Logger initialized")
        conf = cls()
        app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI


config: dict[str, type[Config]] = {
    "default": Config,
}