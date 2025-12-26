from flask import Blueprint

protected_bp = Blueprint("protected", __name__, url_prefix="/protected")

from .import routes