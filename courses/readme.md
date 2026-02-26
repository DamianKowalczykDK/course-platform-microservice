# Courses Microservice

A Python microservice for managing courses, built with Flask, SQLAlchemy, Pydantic, and Dependency Injector.  
It supports CRUD operations for courses and provides a health-check endpoint.

---

## Project Structure
```text
courses/
├── webapp/
│   ├── api/
│   │   ├── courses/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── mappers.py
│   │   └── __init__.py
│   ├── database/
│   │   ├── models/
│   │   │   ├── courses.py
│   │   │   └── __init__.py
│   │   └── repositories/
│   │       ├── courses.py
│   │       ├── generic.py
│   │       └── __init__.py
│   ├── services/
│   │   ├── courses/
│   │   │   ├── dtos.py
│   │   │   ├── mappers.py
│   │   │   └── services.py
│   │   └── __init__.py
│   ├── extensions.py
│   ├── container.py
│   ├── settings.py
│   └──__init__.py
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

- Create, read, update, and delete courses
- Input validation using Pydantic
- Database operations via SQLAlchemy
- Dependency injection for services and repositories
- Custom API exceptions with proper HTTP status codes
- Health check endpoint to verify service and database status

---

## Tech Stack

- Python 3.13
- Flask
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
# Flask / App config
SECRET_KEY=your_secret_key
FLASK_ENV=development

# MySQL (Courses Service)
MYSQL_HOST=your_mysql_courses_host
MYSQL_DATABASE=your_mysql_courses_db
MYSQL_ROOT=your_mysql_root_user
MYSQL_USER=your_mysql_courses_user
MYSQL_PASSWORD=your_mysql_courses_password
MYSQL_ROOT_PASSWORD=your_mysql_root_password
MYSQL_DIALECT=mysql+mysqldb
MYSQL_PORT=your_mysql_port
```
## Poetry
- Install dependencies and activate virtual environment:

```Bash
poetry install
poetry shell
```

## Initialize database
```bash
docker-compose exec courses-webapp flask db init
docker-compose exec courses-webapp flask db migrate -m "Initial migration"
docker-compose exec courses-webapp flask db upgrade
```

## API Endpoints
| Method | Endpoint             | Description                        |
| ------ | -------------------- | ---------------------------------- |
| POST   | `/api/course/`       | Create a new course                |
| GET    | `/api/course/<id>`   | Get a course by ID                 |
| GET    | `/api/course/`       | Get a course by name (query param) |
| PATCH  | `/api/course/<id>`   | Update a course                    |
| DELETE | `/api/course/<id>`   | Delete a course by ID              |
| GET    | `/api/course/health` | Health check (service + DB)        |

## Request / Response Examples
### Create Course
- Request (POST /api/course/):
```JSON
{
  "name": "Python Basics",
  "description": "Learn Python from scratch",
  "price": 199.99,
  "start_date": "2026-03-01T10:00:00",
  "end_date": "2026-03-30T16:00:00",
  "max_participants": 20
}
```
-Response (201 Created):
```JSON
{
  "id": 1,
  "name": "Python Basics",
  "description": "Learn Python from scratch",
  "price": 199.99,
  "start_date": "2026-03-01T10:00:00",
  "end_date": "2026-03-30T16:00:00",
  "max_participants": 20
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
