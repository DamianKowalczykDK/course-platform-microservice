from dotenv import load_dotenv
from typing import TypedDict
from logging.config import dictConfig
from flask import Flask
import os

load_dotenv()

class MongoDBSettings(TypedDict):
    db: str
    host: str
    port: int
    username: str
    password: str

class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', "default secret key")
    FLASK_ENV:str = os.getenv('FLASK_ENV', "development")
    FlASK_DEBUG: bool = os.getenv('FLASK_DEBUG') in ("1", "true", "True")

    MONGODB_DB: str=os.getenv('MONGODB_DB', "")
    MONGODB_HOST: str=os.getenv('MONGODB_HOST', "")
    MONGODB_PORT: int=int(os.getenv('MONGODB_PORT', "27018"))
    MONGODB_USERNAME: str=os.getenv('MONGODB_USERNAME', "")
    MONGODB_PASSWORD: str=os.getenv('MONGODB_PASSWORD', "")

    @property
    def MONGODB_SETTINGS(self) -> MongoDBSettings:
        return {
            'db': self.MONGODB_DB,
            'host': self.MONGODB_HOST,
            'port': self.MONGODB_PORT,
            'username': self.MONGODB_USERNAME,
            'password': self.MONGODB_PASSWORD
        }

    MAIL_SERVER: str=os.getenv('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT: int= int(os.getenv('MAIL_PORT', "587"))
    MAIL_USE_TLS: bool=os.getenv('MAIL_USE_TLS', "True") in ("1", "true", "True")
    MAIL_USE_SSL: bool=os.getenv('MAIL_USE_SSL', "True") in ("1", "true", "True")
    MAIL_USERNAME: str=os.getenv('MAIL_USERNAME', "")
    MAIL_PASSWORD: str=os.getenv('MAIL_PASSWORD', "")
    MAIL_DEFAULT_SENDER: str=os.getenv('MAIL_DEFAULT_SENDER', "")

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

config: dict[str, type[Config]] = {
    "default": Config,
}

