# FastAPI Authentication and RBAC

A production-oriented FastAPI backend for user authentication, refresh-token sessions, role-based access control (RBAC), PostgreSQL persistence, Alembic migrations, and automated API testing.

## Topics Covered

- User registration with username/email uniqueness checks
- Password confirmation and strong-password validation
- Secure password hashing with Passlib and bcrypt
- JWT access tokens and database-backed refresh tokens
- Refresh-token replacement on login, access-token renewal, and logout revocation
- Bearer-token authentication for protected endpoints
- Admin endpoint authentication (`401` without a token) and role-based authorization (`403` for non-admin users)
- Paginated admin user listing with username search, role filtering, active-status filtering, and invalid-page handling
- SQLAlchemy 2.0 ORM models and repository pattern
- Service-layer business logic and dependency injection
- Pydantic request validation and response schemas
- Centralized custom exceptions and application logging
- PostgreSQL schema migrations with Alembic
- Pytest fixtures, dependency overrides, test-database cleanup, and API integration tests
- Refresh-token repository tests for create, lookup, single-token deletion, and user-wide revocation
- GitHub Actions CI with PostgreSQL and migration execution
- Docker and Docker Compose support
- Optional Python basics notes generator using `python-docx`

## Topic Notes and Definitions

### 1. User Registration
- Definition: Creating a new account for a user in the system.
- Note: The app validates uniqueness for the username and email before creating the account.

### 2. Password Confirmation and Validation
- Definition: Ensuring the user enters the same password twice and that the password meets strength rules.
- Note: This reduces accidental typos and improves account security.

### 3. Password Hashing
- Definition: Converting a plain-text password into a one-way encrypted form before storing it.
- Note: The project uses Passlib with bcrypt so passwords cannot be read directly from the database.

### 4. JWT Access Tokens
- Definition: Short-lived tokens used to prove a user is authenticated for API requests.
- Note: Access tokens are issued after login and used in the Authorization header.

### 5. Refresh Tokens
- Definition: Long-lived tokens used to obtain a new access token without requiring the user to log in again.
- Note: Refresh tokens are stored in the database and revoked on logout.

### 6. Bearer-Token Authentication
- Definition: A standard authorization method where a token is sent in the Authorization header.
- Note: Protected routes use the token to identify the current user.

### 7. Role-Based Access Control (RBAC)
- Definition: Restricting access based on a user's assigned role such as user or admin.
- Note: Admin-only endpoints require a valid bearer token and an admin role. Missing authentication returns `401`, while an authenticated non-admin user receives `403`.

### 8. Pagination and Filtering
- Definition: Splitting large result sets into smaller pages and allowing search/filter options.
- Note: The admin user listing supports page size, username search, role filtering, and active-status filtering. A page beyond the available range returns `404 Page not found`.

### 9. SQLAlchemy ORM
- Definition: A Python object-relational mapping layer that lets you work with database records as Python objects.
- Note: The project uses SQLAlchemy models to represent users and refresh tokens.

### 10. Repository Pattern
- Definition: A layer that isolates database queries from business logic.
- Note: Repositories keep data access code organized and easier to test.

### 11. Service Layer
- Definition: The business-logic layer between the API routes and database repositories.
- Note: Services handle authentication flows like registration, login, refresh, and logout.

### 12. Pydantic Schemas
- Definition: Data validation and serialization models used for API request and response payloads.
- Note: Schemas ensure the API receives correct input and returns consistent output.

### 13. Custom Exceptions
- Definition: Application-specific errors used to represent business-rule failures clearly.
- Note: These exceptions are handled centrally to return consistent API responses.

### 14. Alembic Migrations
- Definition: Versioned database schema changes managed through migration scripts.
- Note: Alembic keeps the PostgreSQL database schema aligned with the application models.

### 15. Pytest and Integration Testing
- Definition: Automated tests that validate the real API behavior end to end.
- Note: The project includes fixtures and database cleanup to keep tests isolated.

### 16. GitHub Actions CI
- Definition: Automated workflow execution for running tests and checks on code changes.
- Note: CI helps detect regressions whenever new code is pushed.

### 17. Docker and Docker Compose
- Definition: Container tools used to package and run the app and database together.
- Note: Docker helps create a consistent development and deployment environment.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic 2
- python-jose
- Passlib and bcrypt
- Pytest and pytest-cov
- python-docx
- Docker
- GitHub Actions

## Project Structure

```text
app/
|-- api/
|   |-- admin.py
|   `-- auth.py
|-- core/
|   |-- auth.py
|   |-- config.py
|   |-- exception_handler.py
|   |-- exceptions.py
|   `-- logger.py
|-- db/
|   |-- base.py
|   |-- database.py
|   `-- dependencies.py
|-- dependencies/
|   `-- auth.py
|-- models/
|   |-- refresh_token.py
|   `-- user.py
|-- repositories/
|   |-- refresh_token_repository.py
|   `-- user_repository.py
|-- schemas/
|   |-- common.py
|   `-- user.py
|-- services/
|   |-- auth_service.py
|   `-- user_service.py
|-- utils/
|   `-- security.py
`-- main.py

alembic/
|-- versions/
|-- env.py
`-- script.py.mako

tests/
|-- conftest.py
|-- test_admin.py
|-- test_auth.py
|-- test_database.py
|-- test_exceptions.py
`-- test_repository.py

build_python_basics_notes.py
Python_Basics_Notes.docx
docker-compose.yml
requirements.txt
```

## API Endpoints

### Authentication

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | Public | Register a user with the default `user` role |
| `POST` | `/auth/login` | Public | Authenticate and issue access and refresh tokens |
| `GET` | `/auth/me` | Bearer token | Return the authenticated user |
| `POST` | `/auth/refresh` | Refresh token | Issue a new access token |
| `POST` | `/auth/logout` | Refresh token | Revoke the stored refresh token |

### Admin

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/admin/users` | Admin bearer token | List users with pagination, search, and filters |

Admin query parameters:

| Parameter | Description |
| --- | --- |
| `page` | Page number starting at `1` (default: `1`) |
| `size` | Page size from `1` to `100` (default: `10`) |
| `search` | Optional case-insensitive partial username search |
| `role` | Optional exact role filter |
| `is_active` | Optional active-status filter |

Example:

```http
GET /admin/users?search=lokesh&role=admin&is_active=true&page=1&size=10
Authorization: Bearer <access-token>
```

## Response Format

Standard API responses use this shape:

```json
{
  "success": true,
  "message": "Login Successful",
  "data": {}
}
```

Paginated admin responses include paging information and the applied filters:

```json
{
  "success": true,
  "page": 1,
  "size": 10,
  "total": 25,
  "total_pages": 3,
  "filters": {
    "search": null,
    "role": "admin",
    "is_active": true
  },
  "data": []
}
```

Requests for a page beyond the available range return `404 Page not found`. Authenticated non-admin users receive `403 Admin access required` from admin endpoints.

## Authentication Flow

```text
Register -> Validate input -> Hash password -> Store user
Login -> Verify password -> Replace stored session -> Issue access and refresh tokens
Protected request -> Decode JWT -> Load user -> Allow or deny by role
Refresh -> Validate JWT type and stored token -> Issue a new access token
Logout -> Delete the stored refresh token
```

## Architecture

The application uses a layered design:

```text
Client
  |
  v
FastAPI router and dependencies
  |
  v
Service layer
  |
  v
Repository layer
  |
  v
SQLAlchemy ORM
  |
  v
PostgreSQL
```

- **Routers** handle HTTP input and output.
- **Dependencies** provide database sessions, authenticated users, and admin authorization.
- **Services** contain registration, login, refresh, and logout business logic.
- **Repositories** isolate user and refresh-token database queries.
- **Models and schemas** define persistence entities and validated API contracts.

## Local Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start the API:

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

## Testing

The test suite uses FastAPI's `TestClient` with a database dependency override. Fixtures create unique users, perform registration and login, build bearer headers, and truncate the `users` and `refresh_tokens` tables after each test. Repository tests also use the dedicated test-database session directly and remove the records they create.

Current automated coverage includes:

| Area | Scenarios |
| --- | --- |
| Registration | Successful API registration and reusable registered-user fixture |
| Login | Access-token and refresh-token issuance |
| Login errors | Unknown user returns `404 User not found`; incorrect password returns `401 Invalid credentials` |
| Authentication | Bearer header construction, `/auth/me` current-user lookup, malformed access-token rejection (`401`), and non-numeric token-subject rejection (`401`) |
| Token lifecycle | Successful access-token refresh and logout requests, invalid refresh-token rejection (`401`), and valid but unregistered refresh-token rejection (`404`) |
| Admin authentication and RBAC | Missing-token denial (`401`), regular-user denial (`403`), admin login, bearer-header creation, and successful admin access |
| User listing | Admin retrieval of users, default page `1`, default size `10`, list data, totals, total pages, filter metadata, and combined admin-role filter verification |
| Pagination errors | Out-of-range page returns `404` |
| Search and filters | Username search, admin-role filtering, active-user filtering, and returned filter metadata |
| User repository | User lookup by email, username, and ID; not-found results for each lookup; user creation; and unfiltered user listing |
| Refresh-token repository | Refresh-token creation, invalid-token lookup, single-token deletion, and deleting all refresh tokens for a user |
| Test isolation | Dedicated PostgreSQL session and table cleanup after every test |

The admin tests create admin and regular users directly in the test database because public registration always assigns the `user` role. They then verify `/admin/users` with an authenticated admin, without a token, and with a non-admin token.

Run the full test suite:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Run an individual test module:

```bash
pytest -v tests/test_auth.py
pytest -v tests/test_admin.py
pytest -v tests/test_exceptions.py
pytest -v tests/test_repository.py
```

## Logging

The application logs authentication and token events, including login attempts, successful logins, invalid credentials, refresh-token generation and validation, logout, and authentication-related database failures.

## Python Basics Notes

The repository includes a small utility script that generates a Word document with beginner-friendly Python notes:

```bash
python build_python_basics_notes.py
```

The script uses `python-docx` and writes `Python_Basics_Notes.docx` in the project root.

## CI/CD Pipeline

GitHub Actions runs on pushes and pull requests to `main`:

```text
Checkout -> Set up Python -> Install dependencies -> Start PostgreSQL
         -> Run Alembic migrations -> Execute Pytest
```

The workflow uses a PostgreSQL 17 service and injects database and authentication settings through environment variables and GitHub secrets.

## Docker

Build and start the application stack:

```bash
docker compose up --build
```

Common commands:

```bash
docker compose up -d
docker compose down
docker ps
docker logs fastapi_app
```

## Author

**M. Lokeswara Reddy**

Python Backend Developer
