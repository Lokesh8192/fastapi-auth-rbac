# FastAPI Authentication & Authorization System

## Overview

A secure Authentication and Authorization system built using FastAPI and PostgreSQL. The project implements JWT-based authentication, Role-Based Access Control (RBAC), protected routes, and refresh token management following a layered architecture approach.

## Features

* User Registration with validation
* Secure Password Hashing using bcrypt
* User Login Authentication
* JWT Access Token Generation
* Refresh Token Management
* Protected API Endpoints
* Current User Endpoint (`/auth/me`)
* Role-Based Access Control (RBAC)
* Admin-only APIs
* PostgreSQL Database Integration
* SQLAlchemy ORM
* Dependency Injection
* Structured API Responses

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT (python-jose)
* Passlib (bcrypt)
* Uvicorn
* Git & GitHub

## Project Structure

```text
app/
├── api/
├── core/
├── db/
├── dependencies/
├── models/
├── schemas/
├── services/
└── main.py
```

## Authentication Flow

```text
Register
   ↓
Login
   ↓
Generate JWT Access Token
   ↓
Access Protected Routes
   ↓
Validate Token
   ↓
Return Authenticated User
```

## Authorization Flow

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

## API Endpoints

### Authentication

| Method | Endpoint       | Description          |
| ------ | -------------- | -------------------- |
| POST   | /auth/register | Register a new user  |
| POST   | /auth/login    | Authenticate user    |
| GET    | /auth/me       | Get current user     |
| POST   | /auth/refresh  | Refresh access token |
| POST   | /auth/logout   | Logout user          |

### Admin

| Method | Endpoint     | Description                |
| ------ | ------------ | -------------------------- |
| GET    | /admin/users | Get all users (Admin Only) |

## Database

PostgreSQL is used as the primary database and SQLAlchemy ORM is used for data modeling and database interactions.

## Future Enhancements

* Alembic Database Migrations
* Unit Testing with Pytest
* Docker Containerization
* CI/CD Pipeline
* Cloud Deployment

## Author

Lokeswara Reddy
