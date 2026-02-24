from flask import Flask
from .settings import config
from .extensions import db, migrate
from .container import Container
from .api import api_bp
from .api.error_handlers import register_error_handlers


def create_app() -> Flask:  # pragma: no cover
    """
    Create and configure a Flask application instance.

    This function initializes the Flask app, loads configuration,
    sets up extensions (SQLAlchemy, Migrate), wires the dependency
    injection container, registers error handlers, and registers
    the API blueprint. Logs all routes upon app context initialization.

    Returns:
        Flask: A fully configured Flask application instance ready to run.
    """
    app = Flask(__name__)
    app.config.from_object(config['default'])
    config['default'].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    container = Container()
    container.wire()

    register_error_handlers(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        app.logger.info("[COURSES ROUTES]")
        app.logger.info(app.url_map)

    return app