# 🚀 Courses Microservice
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Production%20Ready-black.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](https://damiankowalczykdk.github.io/course-platform-microservice/courses/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Overview

Courses Microservice is a Python backend service for managing courses in a microservices ecosystem.  
It provides CRUD operations, course search, and a health-check endpoint.  

Key engineering decisions and design principles include:

* **Strict service isolation** – dedicated database and business logic  
* **Dependency injection** with **Dependency Injector**  
* **Input validation** using **Pydantic**  
* **Database operations** via SQLAlchemy ORM  
* Containerized and reproducible via **Docker Compose**  
* Automated migrations with **Flask-Migrate**  
* Full **test coverage** with **Pytest**

---

## 🏗️ Architecture Overview

* **Microservice-based architecture** with REST endpoints  
* **Database layer** with SQLAlchemy ORM for MySQL  
* **Service layer** encapsulating business logic  
* **Centralized exception handling** with proper HTTP responses  
* **Health check endpoint** to monitor service and DB status  

---

## ✨ Technical Highlights & Engineering Decisions

### 🔐 Security & Data Integrity
* Input validation and type checks using Pydantic  
* API exceptions return meaningful HTTP status codes  

### ⚡ Performance & Automation
* Optimized database operations and indexing  
* Non-blocking service design for high concurrency  

### 🧱 Clean Architecture & Maintainability
* Clear separation of API, service, and repository layers  
* Dependency injection for decoupled and testable components  
* Strict type validation with Pydantic  

---

## 💻 Tech Stack

### **Backend**
* Python 3.13  
* Flask  
* Pydantic, Dependency Injector  
* SQLAlchemy, Flask-Migrate  


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

## Initialize database
```bash
docker-compose exec courses-webapp flask db init
docker-compose exec courses-webapp flask db migrate -m "Initial migration"
docker-compose exec courses-webapp flask db upgrade
```

---

## 📥 Request / Response Examples
### Create Course
* **Request** (**POST** **http://localhost/api/course/**):
* **body**
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
* **Response** (**201 Created**):
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
## 📡 API Endpoints
| Method | Endpoint             | Description                        |
| ------ | -------------------- | ---------------------------------- |
| POST   | `/api/course/`       | Create a new course                |
| GET    | `/api/course/<id>`   | Get a course by ID                 |
| GET    | `/api/course/`       | Get a course by name (query param) |
| PATCH  | `/api/course/<id>`   | Update a course                    |
| DELETE | `/api/course/<id>`   | Delete a course by ID              |
| GET    | `/api/course/health` | Health check (service + DB)        |


---
## 📂 Project Structure
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