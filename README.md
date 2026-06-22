# FastAPI Authentication & Authorization System

## Overview

A secure Authentication and Authorization system built using FastAPI and PostgreSQL. The project implements JWT-based authentication, refresh token management, Role-Based Access Control (RBAC), database migrations, exception handling, pagination, search & filtering, and automated testing following a layered architecture approach.

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

### API Features

* Pagination
* Search Users by Username
* Filter Users by Role
* Filter Users by Active Status
* Professional API Response Metadata

### Exception Handling

* Custom Exception Handling
* Global Exception Handling
* Standardized Error Responses
* Centralized Error Management

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
│
├── core/
│   ├── auth.py
│   ├── config.py
│   ├── exceptions.py
│   └── exception_handler.py
│
├── db/
│   ├── database.py
│   ├── dependencies.py
│   └── base.py
│
├── dependencies/
│   └── auth.py
│
├── models/
│   ├── user.py
│   └── refresh_token.py
│
├── schemas/
│   ├── user.py
│   └── common.py
│
├── services/
│   ├── auth_service.py
│   └── user_service.py
│
└── main.py

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

## Pagination Flow

```text
Request
   ↓
page + size
   ↓
Calculate Offset
   ↓
Fetch Records
   ↓
Return Paginated Response
```

### Pagination Parameters

| Parameter | Description         |
| --------- | ------------------- |
| page      | Current Page Number |
| size      | Records Per Page    |

### Sample Response

```json
{
  "success": true,
  "page": 1,
  "size": 5,
  "total": 15,
  "total_pages": 3,
  "data": []
}
```

---

## Search & Filtering

### Search Users

```http
GET /admin/users?search=lokesh
```

### Filter By Role

```http
GET /admin/users?role=admin
```

### Filter By Active Status

```http
GET /admin/users?is_active=true
```

### Combined Query

```http
GET /admin/users?search=lokesh&role=admin&page=1&size=5
```

### Search & Filter Flow

```text
Request
   ↓
Search Filter
   ↓
Role Filter
   ↓
Active Filter
   ↓
Pagination
   ↓
Response
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

| Method | Endpoint     | Description                                    |
| ------ | ------------ | ---------------------------------------------- |
| GET    | /admin/users | Users List with Pagination, Search & Filtering |

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

## Exception Handling

Implemented centralized exception handling for consistent API responses.

### Custom Exceptions

* UserNotFoundException
* InvalidCredentialsException
* RefreshTokenNotFoundException

### Exception Handlers

* Custom exception handlers for business logic errors
* Standardized error response structure
* Improved frontend integration

### Global Exception Handler

* Handles unexpected runtime errors
* Prevents exposing internal server details
* Returns consistent JSON responses

### Error Response Format

```json
{
  "success": false,
  "message": "User not found"
}
```

### Benefits

* Centralized Error Management
* Consistent API Responses
* Better Security
* Improved Maintainability
* Cleaner Service Layer Code

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

### Current Coverage

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
├── Dependency Injection
├── Alembic Migrations
├── API Security
├── Pagination
├── Search & Filtering
├── Exception Handling
├── Global Exception Handling
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

* Logging
* Docker Containerization
* Redis Caching
* Background Tasks
* CI/CD Pipeline
* Cloud Deployment (AWS/Azure)
* API Rate Limiting
* Email Verification
* Password Reset Functionality

---

## Author

**M. Lokeswara Reddy**

Python Backend Developer

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* Backend API Development
* Automated Testing
