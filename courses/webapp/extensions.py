"""
Flask extensions initialization.

This module creates and exposes shared instances of Flask extensions
used across the application:

- `db`: SQLAlchemy instance for ORM operations.
- `migrate`: Flask-Migrate instance for database migrations.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()