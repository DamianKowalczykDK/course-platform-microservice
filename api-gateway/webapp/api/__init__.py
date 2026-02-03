from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .auth import auth_bp
api_bp.register_blueprint(auth_bp)

from .users import users_bp
api_bp.register_blueprint(users_bp)

from .protected import protected_bp
api_bp.register_blueprint(protected_bp)

from .courses import course_bp
api_bp.register_blueprint(course_bp)

