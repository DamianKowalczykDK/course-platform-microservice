# 🚀 Enrolments Microservice
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Production%20Ready-black.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  

---

## 📖 Overview

Enrolments Microservice is a Python backend service for managing course enrolments in a microservices ecosystem.  
It provides CRUD operations, payment tracking, automatic handling of expired enrolments, and a health-check endpoint.  

Key engineering decisions and design principles include:  

* **Strict service isolation** – dedicated database and business logic  
* **Dependency injection** with **Dependency Injector**  
* **Input validation** using **Pydantic**  
* Automated **background tasks** with **APScheduler**  
* Containerized and reproducible via **Docker Compose**  
* Full **test coverage** with **Pytest**

---

## 🏗️ Architecture Overview

* **Microservice-based architecture** with REST endpoints  
* **Database layer** with SQLAlchemy ORM for MySQL  
* **Service layer** encapsulating business logic  
* **Background scheduler** for automated course completion  
* **Centralized exception handling** with proper HTTP responses  

---

## ✨ Technical Highlights & Engineering Decisions

### 🔐 Security & Data Integrity
* Explicit status and payment validation  
* API exceptions return meaningful HTTP status codes  

### ⚡ Performance & Automation
* **APScheduler** automates expiry checks for enrolments  
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
* Flask, Flask-Mail  
* Pydantic, Dependency Injector  
* SQLAlchemy, Flask-Migrate  
* ApScheduler  

### **External Integrations**
* Fakturownia API (invoice generation)  

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

### Initialize database
```bash
docker-compose exec enrolments-webapp flask db init
docker-compose exec enrolments-webapp flask db migrate -m "Initial migration"
docker-compose exec enrolments-webapp flask db upgrade
```
---

## 📥 Request / Response Examples
### Create Enrolment
* **Request** (**POST** **http://localhost/api/enrolment**):
* **body**
```JSON
{
  "course_id": 1,
  "user_id": "63a1f1234abc5678def12345"
}
```
* **Response** (201 Created):
```JSON
{
  "id": 1,
  "user_id": "63a1f1234abc5678def12345",
  "course_id": 1,
  "status": "active",
  "payment_status": "pending",
  "invoice_url": null
}
```
### Set Paid
* **Request** (**PATCH** http://localhost/api/enrolment/paid):
* **body**
```JSON
{
  "enrolment_id": 1
}
```
* **Response** (200 **OK**):
```JSON
{
  "id": 1,
  "user_id": "63a1f1234abc5678def12345",
  "course_id": 1,
  "status": "active",
  "payment_status": "paid",
  "invoice_url": "https://invoice.example.com/123.pdf"
}
```
---
## 📡 API Endpoints
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
---

## 📂 Project Structure
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