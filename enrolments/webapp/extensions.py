from concurrent.futures import ThreadPoolExecutor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
executor = ThreadPoolExecutor(max_workers=2)