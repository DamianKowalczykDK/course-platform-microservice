"""
Course blueprint module.

Defines the `course_bp` Blueprint for all course-related API endpoints,
mounted under the '/course' URL prefix.
"""

from flask import Blueprint

course_bp = Blueprint('course', __name__, url_prefix='/course')