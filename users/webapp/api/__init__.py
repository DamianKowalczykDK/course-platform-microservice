from flask import Blueprint
"""
Main API Blueprint for the application.
"""

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .users import users_bp
api_bp.register_blueprint(users_bp) #type: ignore