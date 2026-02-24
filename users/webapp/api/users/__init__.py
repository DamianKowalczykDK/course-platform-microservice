from flask import Blueprint
"""
Users Blueprint for the Users Microservice.
"""

users_bp = Blueprint('users', __name__, url_prefix='/users')