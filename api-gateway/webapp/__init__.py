from flask import Flask
from .settings import config
from flask_jwt_extended import JWTManager
from .api.error_handlers import register_error_handlers
from .api import api_bp
from .container import Container

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config['default'])
    config['default'].init_app(app)

    jwt = JWTManager()

    jwt.init_app(app)

    container = Container()
    container.wire()

    register_error_handlers(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        app.logger.info("[ API GATEWAY ROUTES]")
        app.logger.info(app.url_map)


    return app