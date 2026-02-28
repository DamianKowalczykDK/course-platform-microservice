# 🚀 Users Microservice
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Production%20Ready-black.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

---

## 📖 Overview

Users Microservice is a Python backend service for managing user accounts in a microservices ecosystem.  
It handles user registration, authentication, password management, and optional MFA (TOTP).  

Key engineering decisions and design principles include:

* **Strict service isolation** – dedicated MongoDB database and business logic  
* **Dependency injection** with **Dependency Injector**  
* **Input validation** using **Pydantic**  
* JWT-based authentication (access + refresh tokens)  
* Optional multi-factor authentication (TOTP)  
* Containerized and reproducible via **Docker Compose**  
* Full **test coverage** with **Pytest**

---

## 🏗️ Architecture Overview

* **Microservice-based architecture** with REST endpoints  
* **Database layer** using MongoEngine (MongoDB)  
* **Service layer** encapsulating business logic  
* **Centralized exception handling** with proper HTTP responses  
* **Health check endpoint** to monitor service and DB status  

---

## ✨ Technical Highlights & Engineering Decisions

### 🔐 Security & Authentication
* JWT authentication (access + refresh tokens)  
* Role-based access control (user/admin)  
* Optional TOTP for MFA  
* Secure password hashing  

### ⚡ Performance & Automation
* Optimized queries and indexing in MongoDB  
* Non-blocking service design for high concurrency  

### 🧱 Clean Architecture & Maintainability
* Clear separation of API, service, and repository layers  
* Dependency injection for decoupled and testable components  
* Strict type validation with Pydantic  

---

## 💻 Tech Stack

### **Backend**
* Python 3.13  
* Flask, Flask-Mail  
* Pydantic, Dependency Injector  
* MongoDB
* PyOTP (TOTP-based MFA)  
* qrcode (QR code generation)  
* Werkzeug (password hashing)  

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
### Create User
* **Request** (**POST** **http://localhost/api/users/**):
* **body**
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
* **Response** (201 Created):
```JSON
{
  "id": "63a1f1234abc5678def12345",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "gender": "Male",
  "role": "user",
  "is_active": false
}
```

### Forgot Password
* **Request** (**POST** **http://localhost/api/users/password/forgot**):
* **body**
```JSON
{
  "identifier": "john@example.com"
}
```
* **Response** (200 OK):
```JSON
{
  "message": "If the email exists, a reset link has been sent."
}
```
---
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

---

## 📂 Project Structure
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