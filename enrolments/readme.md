# Enrolments Microservice

A Python microservice for managing course enrolments, built with Flask, SQLAlchemy, Pydantic, and Dependency Injector.
It supports CRUD operations for enrolments, payment status updates, and provides a health-check endpoint.
---

## Project Structure
```text
enrolments/
├── webapp/
│   ├── api/
│   │   ├── enrolments/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── mappers.py
│   │   └── __init__.py
│   ├── database/
│   │   ├── models/
│   │   │   ├── enrolments.py
│   │   │   └── __init__.py
│   │   └── repositories/
│   │       ├── enrolments.py
│   │       ├── generic.py
│   │       └── __init__.py
│   ├── services/
│   │   ├── enrolments/
│   │   │   ├── dtos.py
│   │   │   ├── mappers.py
│   │   │   └── services.py
│   │   ├── email_service.py
│   │   └── invoices/
│   │       ├── dtos.py
│   │       └── services.py
│   ├── extensions.py
│   ├── container.py
│   ├── settings.py
│   ├── background.py
│   └── __init__.py
├── tests/
│   └── ...
├── .env
├── app.py 
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Environment Variables](#environment-variables)
- [Poetry](#poetry)
- [Initialize database](#initialize-database)
- [API Endpoints](#api-endpoints)
- [Request / Response Examples](#request--response-examples)
- [Testing](#testing)



---

## Features

- Create, read, update, and delete enrolments
- Set enrolment payment status (pending → paid)
- Automatic completion of expired courses
- Input validation using Pydantic
- Database operations via SQLAlchemy
- Dependency injection for services and repositories
- Custom API exceptions with proper HTTP status codes
- Health check endpoint to verify service and database status

---

## Tech Stack

- Python 3.13
- Flask
- Flask-Mail
- ApScheduler
- Fakturownia API
- SQLAlchemy
- Flask-Migrate
- Pydantic
- Dependency Injector
- Poetry
- Docker & Docker Compose

---

## Environment Variables

Create a `.env` file in the root directory. Example:

```env
# Flask / App settings
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
HTTP_TIMEOUT=5

# Database pool settings
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_RECYCLE=1800
DB_POOL_PRE_PING=true

# Enrolments MySQL database
MYSQL_ENROLMENT_HOST=your_mysql_host
MYSQL_ENROLMENT_DATABASE=your_database_name
MYSQL_ENROLMENT_USER=your_db_user
MYSQL_ENROLMENT_PASSWORD=your_db_password
MYSQL_ENROLMENT_ROOT_PASSWORD=your_root_password
MYSQL_ENROLMENT_DIALECT=mysql+mysqldb
MYSQL_ENROLMENT_PORT=your_port

# Mail server settings
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=noreply@example.com

# Service URLs
USERS_SERVICE_URL=http://users-webapp:5000/api/users
COURSE_SERVICE_URL=http://courses-webapp:5000/api/course

# External API / invoice
INVOICE_API_TOKEN=your_invoice_api_token
INVOICE_DOMAIN=your_invoice_domain
```
## Poetry
- Install dependencies and activate virtual environment:

```Bash
poetry install
poetry shell
```

## Initialize database
```bash
docker-compose exec enrolments-webapp flask db init
docker-compose exec enrolments-webapp flask db migrate -m "Initial migration"
docker-compose exec enrolments-webapp flask db upgrade
```

## API Endpoints
| Method | Endpoint                      | Description                          |
| ------ | ----------------------------- | ------------------------------------ |
| POST   | `/api/enrolment/`             | Create a new enrolment               |
| PATCH  | `/api/enrolment/paid`         | Mark enrolment as paid               |
| PATCH  | `/api/enrolment/expired`      | Mark expired enrolments as completed |
| GET    | `/api/enrolment/<id>`         | Get enrolment by ID                  |
| GET    | `/api/enrolment/<id>/details` | Get enrolment by ID and user         |
| GET    | `/api/enrolment/active`       | Get all active enrolments            |
| DELETE | `/api/enrolment/<id>`         | Delete enrolment by ID               |
| GET    | `/api/enrolment/health`       | Health check (service + DB)          |


## Request / Response Examples
### Create Enrolment
- Request (POST /api/enrolment/):
```JSON
{
  "user_id": "user_123",
  "course_id": 1
}
```
-Response (201 Created):
```JSON
{
  "id": 1,
  "user_id": "user_123",
  "course_id": 1,
  "status": "active",
  "payment_status": "pending",
  "invoice_url": null
}
```
### Set Paid
- Request (PATCH /api/enrolment/paid):
```JSON
{
  "enrolment_id": 1
}
```
- Response (200 OK):
```JSON
{
  "id": 1,
  "user_id": "user_123",
  "course_id": 1,
  "status": "active",
  "payment_status": "paid",
  "invoice_url": "https://invoice.example.com/123.pdf"
}
```

## Testing
- - Tests are stored in the `tests/` directory
- Run tests using:
```bash
poetry run pytest
poetry run pytest --cov=webapp --cov-report=html 
```
- Optional: Run static type checks with mypy:
```bash
poetry run mypy .\webapp
```
