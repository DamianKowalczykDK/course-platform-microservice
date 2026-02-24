from flask import Flask
from .settings import config
from .extensions import db, mail
from .container import Container
from .api import api_bp
from .api.error_handlers import register_error_handlers

def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    Sets up configuration, database connection, email service, dependency injection,
    error handlers, and registers the API blueprint.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config['default'])
    config['default'].init_app(app)

    db.connect(
        db=app.config['MONGODB_DB'],
        host=app.config['MONGODB_HOST'],
        port=app.config['MONGODB_PORT'],
        username=app.config['MONGODB_USERNAME'],
        password=app.config['MONGODB_PASSWORD'],
        uuidRepresentation="standard",
    )

    mail.init_app(app)

    container = Container()
    container.wire()

    register_error_handlers(app)
    app.register_blueprint(api_bp)

    return app