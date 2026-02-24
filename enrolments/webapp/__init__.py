from flask import Flask
from .settings import config
from .extensions import db, migrate, mail
from .container import Container
from .api import api_bp
from .api.error_handlers import register_error_handlers
from webapp.background import start_enrolment_expiration_job

def create_app() -> Flask:  # pragma: no cover
    """
    Create and configure the Flask application for the Enrolments microservice.

    This function:
        - Loads configuration from the Config object.
        - Initializes Flask extensions: SQLAlchemy, Flask-Migrate, and Flask-Mail.
        - Sets up dependency injection using the Container.
        - Registers API blueprints and error handlers.
        - Starts the background job for expired enrolments.
        - Logs the application URL map for debugging purposes.

    Returns:
        Flask: A fully configured Flask application instance ready to run.
    """
    app = Flask(__name__)
    app.config.from_object(config['default'])
    config['default'].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    container = Container()
    container.wire()

    register_error_handlers(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        app.logger.info("[ENROLMENTS ROUTES]")
        app.logger.info(app.url_map)
        start_enrolment_expiration_job(app, container)

    return app