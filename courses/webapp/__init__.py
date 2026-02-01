from flask import Flask, current_app
from .settings import config
from .extensions import db,  migrate
from .container import Container
from .api import api_bp
from .api.error_handlers import register_error_handlers

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config['default'])
    config['default'].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    container = Container()
    container.wire()

    register_error_handlers(app)
    app.register_blueprint(api_bp)


    return app