from flask import Blueprint

"""
API Blueprint for the Enrolments microservice.
Registers all enrolment-related routes under the /api prefix.
"""

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .enrolments import enrolment_bp

api_bp.register_blueprint(enrolment_bp)