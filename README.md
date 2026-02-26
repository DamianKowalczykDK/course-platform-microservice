# Course Platform Microservices

A full microservices platform for managing courses, users, and enrolments, with a centralized API Gateway handling authentication, authorization, and request routing.
The system uses MongoDB for users, MySQL for courses and enrolments, and Docker Compose for orchestration.

---

## Project Structure
```text
course-platform/
├── api-gateway/
│   ├── webapp/
│   │   ├── api/
│   │   ├── services/
│   │   ├── container.py
│   │   ├── settings.py
│   │   ├── extensions.py
│   │   └── app.py
│   └── Dockerfile
├── users/
│   ├── webapp/
│   ├── tests/
│   └── Dockerfile
├── courses/
│   ├── webapp/
│   ├── tests/
│   └── Dockerfile
├── enrolments/
│   ├── webapp/
│   ├── tests/
│   └── Dockerfile
├── nginx/
│   └── default.conf
├── docker-compose.yml
├── .env
└── README.md
```
## Microservices

- [Users Service](./users/README.md)
- [Courses Service](./courses/README.md)
- [Enrolments Service](./enrolments/README.md)
- [API Gateway](./api-gateway/README.md)

## Architecture Overview

All traffic goes through the API Gateway, which routes requests to the corresponding microservices.
Authentication, authorization (roles), and MFA are handled centrally in the API Gateway.
```
                   ┌───────────────┐
                   │     Nginx     │
                   │  Port 80      │
                   └──────┬────────┘
                          │
                   ┌──────▼─────────┐
                   │  API Gateway   │
                   │  Port 5000     │
                   └──────┬─────────┘
        ┌───────────────┼───────────────┐
        │               │               │
 ┌──────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
 │ Users MS   │   │ Courses MS│   │ Enrolments│
 │ 5000 /api  │   │ 5000 /api │   │ 5000 /api │
 └──────┬─────┘   └─────┬─────┘   └─────┬─────┘
        │               │               │
 ┌──────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
 │ MongoDB    │   │ MySQL     │   │ MySQL     │
 │ 27017      │   │ 3307      │   │ 3308      │
 └────────────┘   └───────── ─┘   └──────── ──┘
```

## Features

- Central API Gateway routing to microservices
- JWT authentication and refresh tokens (via cookies)
- Role-based access control (admin, user)
- Multi-factor authentication (MFA)
- User management (CRUD, activation, password reset)
- Courses management (CRUD, update, delete)
- Enrolments management (CRUD, paid status, expire)
- Input validation via Pydantic
- Dependency injection via Dependency Injector
- Rate limiting via Flask-Limiter
- Health check endpoints for all services

---

## Tech Stack

- Python 3.13
- Flask (web framework)
- Flask-Mail (email notifications)
- Flask-Limiter (rate limiting)
- Flask-Migrate (database migrations)
- HTTPX (service-to-service communication)
- Flask-JWT-Extended (JWT authentication)
- MongoEngine (Users service)
- SQLAlchemy + MySQL (Courses & Enrolments)
- Pydantic (data validation & serialization)
- Dependency Injector (DI container)
- Docker & Docker Compose (containerization)
- Nginx (reverse proxy)
- Fakturownia API (billing / invoicing)
- AdScheduler (scheduled tasks)

---

## Environment Variables

Create a `.env` file in the root directory. Example:

```env
# =========================
# MongoDB (Users Service)
# =========================
MONGODB_DB=users_db
MONGODB_PORT=27017
MONGODB_USERNAME=your_mongodb_user
MONGODB_PASSWORD=your_mongodb_password

# =========================
# MySQL (Courses Service)
# =========================
MYSQL_DATABASE=courses_db
MYSQL_USER=your_courses_user
MYSQL_PASSWORD=your_courses_password
MYSQL_ROOT=your_root_user
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DIALECT=mysql+mysqldb
MYSQL_PORT=3307

# =========================
# MySQL (Enrolments Service)
# =========================
MYSQL_ENROLMENT_DATABASE=enrolments_db
MYSQL_ENROLMENT_USER=your_enrolments_user
MYSQL_ENROLMENT_PASSWORD=your_enrolments_password
MYSQL_ENROLMENT_ROOT_PASSWORD=your_root_password
MYSQL_ENROLMENT_DIALECT=mysql+mysqldb
MYSQL_ENROLMENT_PORT=3308
```
## Getting Started

### Clone the repository
```bash
git clone https://github.com/DamianKowalczykDK/course-platform-microservice.git
cd course-platform-microservice
```


## Docker Compose

- To start the full platform with all services:
```bash
docker-compose up -d --build
```
- Stop all services:
```bash
docker-compose stop
```
- Check logs:
```bash
docker-compose logs -f api-gateway-webapp
docker-compose logs -f users-webapp
docker-compose logs -f courses-webapp
docker-compose logs -f enrolments-webapp
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

## Test Coverage for All Microservices

All microservices are fully tested with **100% coverage**:

![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)


## Author
![Author](https://img.shields.io/badge/Author-Damian%20Kowalczyk-blue)

## License
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)