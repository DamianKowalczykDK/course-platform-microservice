"""
API blueprint registration module.

Defines the main `api_bp` Blueprint and registers sub-blueprints
(e.g., course routes) under the '/api' prefix.
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .courses import course_bp
api_bp.register_blueprint(course_bp)