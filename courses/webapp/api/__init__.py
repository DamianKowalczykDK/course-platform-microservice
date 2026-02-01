from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .courses import course_bp
api_bp.register_blueprint(course_bp)