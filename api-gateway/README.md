# 🚀 API Gateway
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Production%20Ready-black.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

API Gateway for a microservices ecosystem, built with Python and Flask.  
It routes requests to **Users**, **Courses**, and **Enrolments** microservices, handling authentication, authorization, and request validation.  
Supports JWT authentication, role-based access, and multi-factor authentication (MFA).

---

## 📖 Overview

API Gateway centralizes access to all backend microservices:

* Authenticates users with **JWT** (access + refresh tokens)  
* Handles role-based access (user/admin)  
* Supports optional multi-factor authentication (**TOTP**)  
* Performs request validation and aggregation of service responses  
* Provides a health-check endpoint for monitoring service status  

---

## 🏗️ Architecture Overview

* **REST-based API gateway** for microservices  
* **Service layer** handling HTTP requests to microservices via HTTPX  
* **Centralized exception handling** with proper HTTP status codes  
* **Health check endpoint** monitoring gateway and downstream services  

---

## ✨ Technical Highlights

### 🔐 Security & Authentication
* JWT-based authentication (access + refresh tokens)  
* Role-based access control  
* Optional TOTP MFA  
* Secure handling of tokens and cookies  

### ⚡ Performance & Reliability
* Optimized service-to-service requests with HTTPX  
* Rate limiting with **Flask-Limiter** 
* Non-blocking architecture for high concurrency  

### 🧱 Maintainability
* Clear separation of API routes, services, and DTOs  
* Dependency injection with Dependency Injector  
* Strict request validation with Pydantic  

---

## 💻 Tech Stack

### **Backend**
* Python 3.13  
* Flask  
* Flask-JWT-Extended  
* HTTPX (service-to-service requests)  
* Pydantic  
* Dependency Injector  
* Flask-Limiter

---

## 🚀 Getting Started

### Environment Configuration
* **Copy .env.example to .env and adjust values:** 

```bash
cp .env.example .env
```
### Poetry
* **Install dependencies and activate virtual environment:**

```Bash
poetry install
poetry shell
```
---

## 📥 Request / Response Examples
### Login User
* **Request** (**POST** **http://localhost/api/auth/login**):
* **body**
```JSON
{
  "identifier": "john@example.com",
  "password": "Password1!"
}
```
* **Response** (**200 OK**):
```JSON
{
  "access_token": "jwt-access-token"
}
```
### Notes:
- The refresh token is not included in the response body; it is set as a secure HTTP-only cookie.
- Ensure your client is configured to send cookies for subsequent refresh requests.

## API Endpoints
### Auth
| Method | Endpoint               | Description          |
| ------ | ---------------------- | -------------------- |
| POST   | `/api/auth/login`      | Login user           |
| POST   | `/api/auth/mfa/verify` | Verify MFA code      |
| POST   | `/api/auth/refresh`    | Refresh access token |
| POST   | `/api/auth/logout`     | Logout user          |
### Users
| Method | Endpoint                      | Description                        |
| ------ | ----------------------------- | ---------------------------------- |
| POST   | `/api/users`                  | Create a new user                  |
| PATCH  | `/api/users/activation`       | Activate user with activation code |
| GET    | `/api/users/activation/resend` | Resend activation code             |
| GET    | `/api/users/identifier`       | Get user by username/email         |
| GET    | `/api/users/id`               | Get user by ID                     |
| POST   | `/api/users/password/forgot`  | Request password reset link        |
| POST   | `/api/users/password/reset`   | Reset password with token          |
| PATCH  | `/api/users/mfa/enable`       | Enable MFA and get QR code         |
| PATCH  | `/api/users/mfa/disable`      | Disable MFA                        |
| GET    | `/api/users/mfa/qr`           | Get MFA QR code                    |
| DELETE | `/api/users/id`               | Delete user by ID                  |
| DELETE | `/api/users/identifier`       | Delete user by username/email      |
### Courses
| Method | Endpoint          | Description        |
| ------ | ----------------- | ------------------ |
| POST   | `/api/course/`    | Create a course    |
| GET    | `/api/course/<id>` | Get course by ID   |
| GET    | `/api/course/`    | Get course by name |
| PATCH  | `/api/course/<id>` | Update course      |
| DELETE | `/api/course/<id>` | Delete course      |
### Enrolments
| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| POST   | `/api/enrolment`        | Enrol user in course           |
| PATCH  | `/api/enrolment/paid`   | Mark enrolment as paid         |
| PATCH  | `/api/enrolment/expired` | Expire courses (admin only)    |
| GET    | `/api/enrolment/<id>`   | Get enrolment by ID (admin)    |
| GET    | `/api/enrolment/<id>/details` | Get enrolment by ID & user     |
| GET    | `/api/enrolment/active` | Get all active enrolments      |
| DELETE | `/api/enrolment/<id>`   | Delete enrolment by ID (admin) |

## 📂 Project Structure
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