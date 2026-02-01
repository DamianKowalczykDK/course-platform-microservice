from urllib.parse import quote_plus
from dotenv import load_dotenv
from typing import TypedDict
from logging.config import dictConfig
from flask import Flask
import os

load_dotenv()


class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', "default secret key")
    FLASK_ENV:str = os.getenv('FLASK_ENV', "development")
    FlASK_DEBUG: bool = os.getenv('FLASK_DEBUG') in ("1", "true", "True")

    MYSQL_DIALECT: str = os.getenv('MYSQL_DIALECT', 'mysql+mysqldb')
    MYSQL_HOST: str = os.getenv('MYSQL_HOST', 'mysql-courses')
    MYSQL_DATABASE: str = os.getenv('MYSQL_DATABASE', 'db_courses')
    MYSQL_USER: str = os.getenv('MYSQL_USER', '')
    MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_ROOT_PASSWORD: str = os.getenv('MYSQL_ROOT_PASSWORD', '')
    MYSQL_PORT: str = os.getenv('MYSQL_PORT', '3307')

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"{self.MYSQL_DIALECT}://{self.MYSQL_USER}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )

    # MAIL_SERVER: str=os.getenv('MAIL_SERVER', "smtp.gmail.com")
    # MAIL_PORT: int= int(os.getenv('MAIL_PORT', "587"))
    # MAIL_USE_TLS: bool=os.getenv('MAIL_USE_TLS', "True") in ("1", "true", "True")
    # MAIL_USE_SSL: bool=os.getenv('MAIL_USE_SSL', "False") in ("1", "true", "True")
    # MAIL_USERNAME: str=os.getenv('MAIL_USERNAME', "")
    # MAIL_PASSWORD: str=os.getenv('MAIL_PASSWORD', "")
    # MAIL_DEFAULT_SENDER: str=os.getenv('MAIL_DEFAULT_SENDER', "")

    @staticmethod
    def configure_logging(app: Flask) -> None:
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
    def init_app(cls, app: Flask) -> None:
        cls.configure_logging(app)
        app.logger.debug("Logger initialized")
        conf = cls()
        app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cls.SQLALCHEMY_TRACK_MODIFICATIONS
        # app.config['SQLALCHEMY_ENGINE_OPTIONS'] = cls.SQLALCHEMY_ENGINE_OPTIONS

config: dict[str, type[Config]] = {
    "default": Config,
}


