from flask import Flask
from .settings import config
from .extensions import db, mail

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(config['default'])
    db.connect(
        db=app.config["MONGODB_DB"],
        host=app.config["MONGODB_HOST"],
        port=app.config["MONGODB_PORT"],
        username=app.config["MONGODB_USERNAME"],
        password=app.config["MONGODB_PASSWORD"],
    )

    mail.init_app(app)

    config["default"].init_app(app)

    return app
