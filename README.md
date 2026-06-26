# FastAPI Authentication and RBAC

A production-oriented FastAPI backend that provides user authentication, refresh-token sessions, role-based access control, PostgreSQL persistence, Alembic migrations, Docker support, and automated tests.

## Features

- User registration with password confirmation and validation
- Secure password hashing with bcrypt
- JWT access tokens and refresh-token management
- Logout by refresh-token invalidation
- Protected current-user endpoint
- Admin-only user listing with pagination, search, and filters
- SQLAlchemy ORM models and Alembic migrations
- Centralized exception handling and consistent API responses
- Application logging for authentication and database events
- Pytest-based API tests with database cleanup fixtures
- Docker and Docker Compose support

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- python-jose
- Passlib and bcrypt
- Pytest
- Docker

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
|-- test_auth.py
`-- test_database.py
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Authenticate and issue tokens |
| `GET` | `/auth/me` | Return the authenticated user |
| `POST` | `/auth/refresh` | Issue a new access token |
| `POST` | `/auth/logout` | Revoke a refresh token |

### Admin

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/admin/users` | List users with pagination, search, and filters |

Admin query parameters:

| Parameter | Description |
| --- | --- |
| `page` | Page number, starting at `1` |
| `size` | Page size, from `1` to `100` |
| `search` | Optional username search |
| `role` | Optional role filter |
| `is_active` | Optional active-status filter |

Example:

```http
GET /admin/users?search=lokesh&role=admin&is_active=true&page=1&size=10
```

## Response Format

Standard API responses use the following shape:

```json
{
  "success": true,
  "message": "Login Successful",
  "data": {}
}
```

Paginated admin responses include pagination metadata:

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

## Authentication Flow

```text
Register -> Hash Password -> Store User
Login -> Verify Password -> Issue Access Token and Refresh Token
Protected Request -> Validate JWT -> Load Current User -> Allow or Deny
Refresh -> Validate Refresh Token -> Issue New Access Token
Logout -> Delete Refresh Token
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_auth_rbac
TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_auth_rbac_test
SECRET_KEY=change-this-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
alembic upgrade head
```

4. Start the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Docker

Build and run the application stack:

```bash
docker compose up --build
```

Common Docker commands:

```bash
docker compose up -d
docker compose down
docker ps
docker logs fastapi_app
```

## Testing

Run the test suite:

```bash
pytest -v
```

Run coverage:

```bash
pytest --cov=app
```

## Logging

The application logs authentication and token events, including:

- Login attempts and successful logins
- Invalid password attempts
- Refresh-token generation and validation
- Logout events
- Database errors during authentication workflows

## Author

**M. Lokeswara Reddy**

Python Backend Developer
