from flask import Flask
from .settings import config
from .extensions import db,  migrate, mail
from .container import Container
from .api import api_bp
from .api.error_handlers import register_error_handlers
from webapp.background import start_enrolment_expiration_job

def create_app() -> Flask: # pragma: no cover
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