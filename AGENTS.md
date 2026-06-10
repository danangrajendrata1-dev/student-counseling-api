# AGENTS.md — Student Counseling Backend API

## Project Mission

Build a clean, secure, and maintainable FastAPI backend API for a school counseling management system.

This project is intended as a professional Junior Backend Developer Python portfolio project.

---

## Main Rules

1. Do not make large refactors without explicit approval.
2. Do not rename folders or files without clear reason.
3. Do not change database schema without updating docs/DATABASE_SCHEMA.md and Alembic migration.
4. Do not hardcode secrets, database URLs, JWT secrets, or production URLs.
5. Always use environment variables for configuration.
6. Keep code clean, modular, and readable.
7. Follow route-service-repository structure.
8. Do not place business logic directly inside route files.
9. Do not expose hashed_password in API responses.
10. Do not create frontend code unless explicitly requested.

---

## Architecture Rules

Use this flow:

```txt
route → service → repository → database
```

Responsibilities:

- routes: HTTP request and response.
- schemas: request and response validation.
- services: business logic and permission logic.
- repositories: database query.
- models: SQLAlchemy database models.
- core: config, security, permissions.
- utils: reusable helper functions.

---

## Backend Stack

Use:

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- JWT
- bcrypt
- Pytest

Do not introduce unnecessary frameworks.

---

## Security Rules

1. Password must be hashed.
2. JWT secret must come from env.
3. Protected endpoints must check current user.
4. Role-based access must be enforced.
5. Student can only access their own confession.
6. Principal can only access aggregate reports.
7. Do not expose sensitive data to unauthorized roles.
8. Do not return internal traceback to API clients.
9. Do not commit .env.

---

## Coding Style

1. Use clear function names.
2. Keep functions small and single-purpose.
3. Use type hints where possible.
4. Avoid duplicated logic.
5. Use constants or enums for roles and statuses.
6. Use explicit error handling.
7. Keep response format consistent.
8. Add comments only when they clarify important logic.

---

## Testing Rules

Add or update tests for:

1. Authentication.
2. Authorization.
3. Student CRUD.
4. Confession ownership.
5. Report access.
6. Pagination and filters.

Do not skip tests for security-sensitive changes.

---

## Documentation Rules

When adding or changing features, update relevant docs:

- docs/PRD.md
- docs/TECHNICAL_DESIGN.md
- docs/DATABASE_SCHEMA.md
- docs/SECURITY_RULES.md
- README.md

---

## Scope Control

MVP does not include:

- Frontend.
- File upload.
- PDF export.
- Excel import.
- WhatsApp integration.
- AI analysis.
- Realtime chat.
- Multi-school support.

Do not add these features unless explicitly requested.
