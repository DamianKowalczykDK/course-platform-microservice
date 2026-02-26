# API Gateway

A Python API Gateway built with Flask, HTTPX, and Dependency Injector.
It routes requests to microservices for users, courses, and enrolments, handling authentication, authorization, and validation.
Supports JWT authentication, role-based access, multi-factor authentication (MFA), and service aggregation.

---

## Project Structure
```text
api-gateway/
├── webapp/
│   ├── api/
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── mappers.py
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── mappers.py
│   │   ├── courses/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── mappers.py
│   │   ├── enrolments/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── mappers.py
│   │   └── protected/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── services/
│   │   ├── auth/
│   │   │   ├── dtos.py
│   │   │   └── services.py
│   │   ├── users/
│   │   │   ├── dtos.py
│   │   │   └── services.py
│   │   ├── courses/
│   │   │   ├── dtos.py
│   │   │   └── services.py
│   │   └── enrolments/
│   │       ├── dtos.py
│   │       └── services.py
│   ├── extensions.py
│   ├── settings.py
│   ├── container.py
│   ├── __init__.py
│   ├── tests/
│   
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
- [API Endpoints](#api-endpoints)
- [Request / Response Examples](#request--response-examples)
- [Testing](#testing)



---

## Features

- Central gateway for users, courses, and enrolments microservices
- JWT authentication and refresh tokens
- Role-based access control (admin, user)
- Multi-factor authentication (MFA) support
- Input validation using Pydantic
- Service-to-service HTTP communication via HTTPX
- Dependency injection using Dependency Injector
- Error handling with proper HTTP status codes
- Health check endpoint

---

## Tech Stack

- Python 3.13
- Flask
- HTTPX (service requests)
- Flask-JWT-Extended (JWT authentication)
- Pydantic
- Dependency Injector
- Flask-Limiter (rate limiting)
- Poetry
- Docker & Docker Compose

---

## Environment Variables

Create a `.env` file in the root directory. Example:

```env
# =========================
# Flask / App config
# =========================
SECRET_KEY=your_secret_key
FLASK_ENV=development
HTTP_TIMEOUT=5

# =========================
# JWT / Auth config
# =========================
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ACCESS_TOKEN_EXPIRES=300
JWT_REFRESH_TOKEN_EXPIRES=3600
JWT_COOKIE_CSRF_PROTECT=False
JWT_ALGORITHM=HS512

JWT_TOKEN_LOCATION=cookies,headers
JWT_TOKEN_SECURE=True
JWT_TOKEN_SAMESITE=Strict

# =========================
# Microservices URLs
# =========================
USERS_SERVICE_URL=http://users-webapp:5000/api/users
COURSE_SERVICE_URL=http://courses-webapp:5000/api/course
ENROLMENT_SERVICE_URL=http://enrolments-webapp:5000/api/enrolment

# =========================
# CORS config
# =========================
CORS_ORIGINS=["http://localhost:3000"]
CORS_METHODS=["GET", "POST", "PATCH", "OPTIONS"]
CORS_HEADERS=["Content-Type", "Authorization"]
```
## Poetry
- Install dependencies and activate virtual environment:

```Bash
poetry install
poetry shell
```


## API Endpoints
### Auth
| Method | Endpoint               | Description          |
| ------ | ---------------------- | -------------------- |
| POST   | `/api/auth/login`      | Login user           |
| POST   | `/api/auth/mfa/verify` | Verify MFA code      |
| POST   | `/api/auth/refresh`    | Refresh access token |
| POST   | `/api/auth/logout`     | Logout user          |
### Users
| Method | Endpoint                       | Description                        |
| ------ | ------------------------------ | ---------------------------------- |
| POST   | `/api/users/`                  | Create a new user                  |
| PATCH  | `/api/users/activation`        | Activate user with activation code |
| GET    | `/api/users/activation/resend` | Resend activation code             |
| GET    | `/api/users/identifier`        | Get user by username/email         |
| GET    | `/api/users/id`                | Get user by ID                     |
| POST   | `/api/users/password/forgot`   | Request password reset link        |
| POST   | `/api/users/password/reset`    | Reset password with token          |
| PATCH  | `/api/users/mfa/enable`        | Enable MFA and get QR code         |
| PATCH  | `/api/users/mfa/disable`       | Disable MFA                        |
| GET    | `/api/users/mfa/qr`            | Get MFA QR code                    |
| DELETE | `/api/users/id`                | Delete user by ID                  |
| DELETE | `/api/users/identifier`        | Delete user by username/email      |
### Courses
| Method | Endpoint          | Description        |
| ------ | ----------------- | ------------------ |
| POST   | `/api/course/`    | Create a course    |
| GET    | `/api/course/<id>` | Get course by ID   |
| GET    | `/api/course/`    | Get course by name |
| PATCH  | `/api/course/<id>` | Update course      |
| DELETE | `/api/course/<id>` | Delete course      |
### Enrolments
| Method | Endpoint                 | Description                    |
| ------ | ------------------------ | ------------------------------ |
| POST   | `/api/enrolment/`        | Enrol user in course           |
| PATCH  | `/api/enrolment/paid`    | Mark enrolment as paid         |
| PATCH  | `/api/enrolment/expired` | Expire courses (admin only)    |
| GET    | `/api/enrolment/<id>`    | Get enrolment by ID (admin)    |
| GET    | `/api/enrolment/<id>/details` | Get enrolment by ID & user     |
| GET    | `/api/enrolment/active`  | Get all active enrolments      |
| DELETE | `/api/enrolment/<id>`    | Delete enrolment by ID (admin) |

## Request / Response Examples
### Login User
- Request (POST /api/auth/login):
- Rate Limit: 2 requests per minute per IP
```JSON
{
  "identifier": "john@example.com",
  "password": "Password1!"
}
```
-Response (200 OK):
```JSON
{
  "access_token": "jwt-access-token"
}
```
### Notes:
- The refresh token is not included in the response body; it is set as a secure HTTP-only cookie.
- Ensure your client is configured to send cookies for subsequent refresh requests.

## Testing
- Tests are stored in the `tests/` directory
- Run tests using:
```bash
poetry run pytest
poetry run pytest --cov=webapp --cov-report=html 
```
- Optional: Run static type checks with mypy:
```bash
poetry run mypy .\webapp
```
