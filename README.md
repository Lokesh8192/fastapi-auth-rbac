<img width="960" height="540" alt="Screenshot 2026-06-18 183409" src="https://github.com/user-attachments/assets/25dad06b-0681-4645-b946-9751e84d1fca" />
<img width="960" height="540" alt="Screenshot 2026-06-18 183300" src="https://github.com/user-attachments/assets/54a390b0-4ec7-45ac-b55d-d13885aa087c" />
# FastAPI Authentication & Authorization System

## Overview

A secure Authentication and Authorization system built using FastAPI and PostgreSQL. The project implements JWT-based authentication, refresh token management, Role-Based Access Control (RBAC), database migrations, and automated testing following a layered architecture approach.

---

## Features

### Authentication

* User Registration with Validation
* Secure Password Hashing using bcrypt
* User Login Authentication
* JWT Access Token Generation
* Refresh Token Management
* Logout Functionality
* Protected API Endpoints
* Current User Endpoint (`/auth/me`)

### Authorization

* Role-Based Access Control (RBAC)
* Admin-only API Access
* Current User Authentication
* Route Protection using Dependencies

### Database

* PostgreSQL Integration
* SQLAlchemy ORM
* Alembic Database Migrations
* Database Session Management

### Testing

* Automated API Testing using Pytest
* FastAPI TestClient
* Test Database Setup
* Dependency Override for Testing
* Reusable Fixtures
* Automatic Database Cleanup
* Coverage Reporting

---

## Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic

### Authentication & Security

* JWT (python-jose)
* Passlib (bcrypt)
* RBAC

### Database Management

* Alembic Migrations

### Testing

* Pytest
* FastAPI TestClient
* pytest-cov

### Tools

* Git
* GitHub
* pgAdmin
* VS Code

---

## Project Structure

```text
app/
├── api/
│   ├── auth.py
│   └── admin.py
├── core/
│   ├── auth.py
│   ├── config.py
│   └── security.py
├── db/
│   ├── database.py
│   ├── dependencies.py
│   └── base.py
├── dependencies/
│   └── auth.py
├── models/
│   ├── user.py
│   └── refresh_token.py
├── schemas/
│   ├── user.py
│   └── common.py
├── services/
│   ├── user_service.py
│   └── auth_service.py
├── main.py

tests/
├── conftest.py
├── test_auth.py
└── test_database.py

alembic/
```

---

## Authentication Flow

```text
Register
   ↓
Password Hashing
   ↓
Store User
   ↓
Login
   ↓
Generate Access Token
   ↓
Generate Refresh Token
   ↓
Access Protected Routes
```

---

## Refresh Token Flow

```text
Login
   ↓
Access Token + Refresh Token
   ↓
Access Token Expires
   ↓
Refresh Endpoint
   ↓
Generate New Access Token
```

---

## RBAC Flow

```text
User Login
    ↓
JWT Validation
    ↓
Get Current User
    ↓
Role Verification
    ↓
Allow / Deny Access
```

---

## API Endpoints

### Authentication

| Method | Endpoint       | Description          |
| ------ | -------------- | -------------------- |
| POST   | /auth/register | Register User        |
| POST   | /auth/login    | Login User           |
| GET    | /auth/me       | Current User         |
| POST   | /auth/refresh  | Refresh Access Token |
| POST   | /auth/logout   | Logout User          |

### Admin

| Method | Endpoint     | Description                |
| ------ | ------------ | -------------------------- |
| GET    | /admin/users | Get All Users (Admin Only) |

---

## Database Schema

### Users

```text
id
username
email
hashed_password
role
is_active
created_at
```

### Refresh Tokens

```text
id
user_id
token
expires_at
```

---

## Testing

### Testing Stack

* Pytest
* FastAPI TestClient
* pytest-cov

### Implemented Tests

* User Registration
* User Login
* JWT Authentication
* Protected Routes
* Refresh Token Flow
* Logout Functionality
* RBAC Authorization

### Test Infrastructure

* Dedicated Test Database
* Dependency Override
* Fixtures
* Fixture Chaining
* Yield Fixtures
* Automatic Cleanup

### Run Tests

```bash
pytest -v
```

### Run Coverage

```bash
pytest --cov
```

Current Coverage:

```text
79%
```

---

## Concepts Implemented

```text
Backend Development
├── FastAPI
├── PostgreSQL
├── SQLAlchemy
├── Pydantic
├── JWT Authentication
├── Refresh Tokens
├── RBAC
├── Alembic Migrations
├── Dependency Injection
├── API Security
├── Git & GitHub
└── Pytest Testing

Testing
├── Fixtures
├── Fixture Chaining
├── Test Database
├── Dependency Override
├── Yield Fixtures
├── Automatic Cleanup
└── Coverage Reports
```

---

## Future Enhancements

* Custom Exception Handlers
* Pagination
* Search & Filtering
* Logging
* Docker
* CI/CD Pipeline
* Cloud Deployment

---

## Author
**M.Lokeswara Reddy**
Python Backend Developer
Lokeswara Reddy
