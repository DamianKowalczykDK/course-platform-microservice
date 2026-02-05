from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .enrolments import enrolment_bp

api_bp.register_blueprint(enrolment_bp)
