from dotenv import load_dotenv
from logging.config import dictConfig
from flask import Flask
import os

load_dotenv()


class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', "")
    FLASK_ENV:str = os.getenv('FLASK_ENV', "")
    FlASK_DEBUG: bool = os.getenv('FLASK_DEBUG') in ("1", "true", "True")
    HTTP_TIMEOUT: int = int(os.getenv("HTTP_TIMEOUT", ""))

    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', "")
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', ""))
    JWT_REFRESH_TOKEN_EXPIRES: int = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', ""))
    JWT_COOKIE_CSRF_PROTECT: bool = os.getenv("JWT_COOKIE_CSRF_PROTECT", "False") in ("1", "true", "True")
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
    JWT_TOKEN_LOCATION: list[str] = os.getenv('JWT_TOKEN_LOCATION', "cookies, headers").split(",")
    # JWT_TOKEN_SECURE: bool = os.getenv('JWT_TOKEN_SECURE', "True") in ("1", "true", "True")
    # JWT_TOKEN_SAMESITE: str = os.getenv('JWT_TOKEN_SAMESITE', "")

    USERS_SERVICE_URL: str = os.getenv('USERS_SERVICE_URL', "")
    COURSE_SERVICE_URL: str = os.getenv('COURSE_SERVICE_URL', "")
    ENROLMENT_SERVICE_URL: str = os.getenv('ENROLMENT_SERVICE_URL', "")

    CORS_ORIGINS: list[str] = os.getenv('CORS_ORIGINS', "[]").split(",")
    CORS_METHODS: list[str] = os.getenv('CORS_METHODS', "[]").split(",")
    CORS_HEADERS: list[str] = os.getenv('CORS_HEADERS', "[]").split(",")

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

