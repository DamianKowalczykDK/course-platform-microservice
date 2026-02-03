from typing import Generator
from flask import Flask, Response
from sqlalchemy import StaticPool
from webapp import api_bp, register_error_handlers, create_app
from webapp.extensions import db
from webapp.container import Container
import pytest


@pytest.fixture(autouse=True)
def app() -> Generator[Flask, None, None]:
    application = Flask(__name__)
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        }
    )
    db.init_app(application)

    container: Container = Container()
    container.wire(packages=["webapp.api.courses"])

    application.register_blueprint(api_bp)

    register_error_handlers(application)

    @application.after_request
    def cleanup(response: Response) -> Response:
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.remove()
        return response

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()
        db.engine.dispose()