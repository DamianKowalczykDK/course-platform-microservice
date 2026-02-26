# Users Microservice

A Python microservice for managing users, built with Flask, MongoEngine, Pydantic, and Dependency Injector.  
It supports user registration, activation, authentication, password management, multi-factor authentication (MFA), and provides a health-check endpoint.

---

## Project Structure
```text
users/
├── webapp/
│   ├── api/
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── mappers.py
│   │   └── __init__.py
│   ├── database/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   └── repositories/
│   │       ├── user.py
│   │       └── __init__.py
│   ├── services/
│   │   ├── users/
│   │   │   ├── dtos.py
│   │   │   ├── mappers.py
│   │   │   └── services.py
│   │   ├── email_service.py
│   │   └── exceptions.py
│   ├── extensions.py
│   ├── container.py
│   ├── settings.py
│   ├── __init__.py
│   ├── tests/
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
- [API Endpoints](#api-endpoints)
- [Request / Response Examples](#request--response-examples)
- [Testing](#testing)



---

## Features

- User registration with email activation
- Authentication (login) with password hashing
- Password reset with token expiration
- Multi-factor authentication (MFA) enable/disable with QR code
- Get user by ID or username/email
- Delete users by ID or identifier
- Input validation using Pydantic
- Database operations via MongoEngine
- Dependency injection for services and repositories
- Custom API exceptions with proper HTTP status codes
- Health check endpoint to verify service and database status

---

## Tech Stack

- Python 3.13
- Flask
- Flask-Mail
- MongoEngine
- Pydantic
- PyOTP (TOTP-based MFA)
- qrcode (QR code generation)
- Werkzeug (password hashing)
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
FLASK_DEBUG=True

# User activation & password reset
USER_ACTIVATION_EXPIRATION_MINUTES=60
RESET_PASSWORD_EXPIRATION_MINUTES=15

# MongoDB settings
MONGODB_DB=users_db
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password

# Mail server settings
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_DEFAULT_SENDER=noreply@example.com
```
## Poetry
- Install dependencies and activate virtual environment:

```Bash
poetry install
poetry shell
```


## API Endpoints
| Method | Endpoint                       | Description                          |
| ------ | ------------------------------ | ------------------------------------ |
| POST   | `/api/users/`                  | Create a new user                    |
| PATCH  | `/api/users/activation`        | Activate a user with activation code |
| GET    | `/api/users/activation/resend` | Resend activation code to user       |
| GET    | `/api/users/identifier`        | Get active user by username or email |
| GET    | `/api/users/id`                | Get user by ID                       |
| POST   | `/api/users/auth/check`        | Verify login credentials             |
| POST   | `/api/users/password/forgot`   | Request password reset link          |
| POST   | `/api/users/password/reset`    | Reset password with token            |
| PATCH  | `/api/users/mfa/enable`        | Enable MFA for user and get QR code  |
| PATCH  | `/api/users/mfa/disable`       | Disable MFA for user                 |
| GET    | `/api/users/mfa/qr`            | Get MFA QR code for user             |
| DELETE | `/api/users/id`                | Delete user by ID                    |
| DELETE | `/api/users/identifier`        | Delete user by username or email     |
| GET    | `/api/users/health`            | Health check (service + database)    |


## Request / Response Examples
### Create User
- Request (POST /api/users/):
```JSON
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "Password1!",
  "password_confirmation": "Password1!",
  "gender": "Male",
  "role": "user"
}
```
-Response (201 Created):
```JSON
{
  "id": "63a1f1234abc5678def12345",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "gender": "Male",
  "role": "user",
  "is_active": false,
  "mfa_secret": null
}
```
### Forgot Password
- Request (POST /api/users/password/forgot):

```JSON
{
  "identifier": "john@example.com"
}
```
- Response (200 OK):
```JSON
{
  "message": "If the email exists, a reset link has been sent."
}
```

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
