# FastAPI Authentication and RBAC

A production-oriented FastAPI backend for user authentication, refresh-token sessions, role-based access control (RBAC), PostgreSQL persistence, Alembic migrations, and automated API testing.

## Topics Covered

- User registration with username/email uniqueness checks
- Password confirmation and strong-password validation
- Secure password hashing with Passlib and bcrypt
- JWT access tokens and database-backed refresh tokens
- Refresh-token replacement on login, access-token renewal, and logout revocation
- Bearer-token authentication for protected endpoints
- Role-based authorization for admin-only operations
- Paginated user listing with username search, role filtering, and active-status filtering
- SQLAlchemy 2.0 ORM models and repository pattern
- Service-layer business logic and dependency injection
- Pydantic request validation and response schemas
- Centralized custom exceptions and application logging
- PostgreSQL schema migrations with Alembic
- Pytest fixtures, dependency overrides, test-database cleanup, and API integration tests
- GitHub Actions CI with PostgreSQL and migration execution
- Docker and Docker Compose support

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic 2
- python-jose
- Passlib and bcrypt
- Pytest and pytest-cov
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
`-- test_database.py
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
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create the application and test PostgreSQL databases and configure `.env`.
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

The test suite uses FastAPI's `TestClient` with a database dependency override. Fixtures create unique users, perform registration and login, build bearer headers, and truncate the `users` and `refresh_tokens` tables after each test.

Current automated coverage includes:

| Area | Scenarios |
| --- | --- |
| Registration | Successful API registration and reusable registered-user fixture |
| Login | Access-token and refresh-token issuance |
| Authentication | Bearer header construction and `/auth/me` current-user lookup |
| Token lifecycle | Successful access-token refresh and logout requests |
| RBAC | Regular-user denial (`403`) and successful admin access |
| User listing | Default pagination fields and response structure |
| Pagination errors | Out-of-range page returns `404` |
| Search and filters | Username search, role filtering, and returned filter metadata |
| Test isolation | Dedicated PostgreSQL session and table cleanup after every test |

Run the full test suite:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Run only authentication or admin tests:

```bash
pytest -v tests/test_auth.py
pytest -v tests/test_admin.py
```

## Logging

The application logs authentication and token events, including login attempts, successful logins, invalid credentials, refresh-token generation and validation, logout, and authentication-related database failures.

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
