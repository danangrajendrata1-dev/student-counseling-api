# Student Counseling API / BK Smart Core API

[![CI](https://github.com/danangrajendrata1-dev/student-counseling-api/actions/workflows/ci.yml/badge.svg)](https://github.com/danangrajendrata1-dev/student-counseling-api/actions/workflows/ci.yml)

A professional backend API for a school counseling management system, built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, role-based authorization, and automated testing.

This project is developed as a Junior Backend Developer Python portfolio project, focusing on clean architecture, maintainable code structure, secure authentication, database migrations, and test coverage.

## Project Goals

The goal of this project is to demonstrate backend development skills such as:

* Building RESTful APIs with FastAPI
* Managing relational data with PostgreSQL and SQLAlchemy
* Handling database migrations with Alembic
* Implementing JWT-based authentication
* Implementing role-based access control
* Separating backend layers using routes, services, repositories, schemas, and models
* Writing automated tests with Pytest
* Preparing the project for production-style development and future Docker deployment

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* python-jose / JWT
* passlib bcrypt
* Pytest
* Docker

## Main Features

### Authentication

* User registration
* User login
* JWT access token generation
* Get current authenticated user with `/auth/me`
* Password hashing with bcrypt
* Duplicate email validation
* Invalid credential handling

### Role-Based Authorization

Supported roles:

* `admin`
* `counselor`
* `student`
* `principal`

Authorization is handled using reusable role permission dependencies.

### Student Management

* Create student
* List students
* Get student detail
* Update student
* Delete student

Access rules:

* Admin and counselor can manage students
* Only admin can delete students
* Student and principal cannot access internal student CRUD endpoints

### Counseling Records

* Create counseling record
* List counseling records
* Get counseling record detail
* Update counseling record
* Delete counseling record

Access rules:

* Admin and counselor can manage counseling records
* Student and principal cannot access counseling record detail endpoints

### Assessments

* Create assessment
* List assessments
* Get assessment detail
* Update assessment
* Delete assessment

Access rules:

* Admin and counselor can manage assessments
* Student and principal cannot access assessment detail endpoints

### Reports Summary

* Get aggregate report summary
* Count total students
* Count active students
* Count counseling records
* Count assessments
* Group counseling records by type and status
* Group assessments by type and status

Access rules:

* Admin, counselor, and principal can access report summary
* Student cannot access report summary

## Architecture

This project uses a clean layered backend architecture:

```txt
route -> service -> repository -> database
```

Layer responsibilities:

```txt
routes        : Handle HTTP requests and responses
schemas       : Validate request and response data
services      : Hold business logic
repositories  : Handle database queries
models        : Define SQLAlchemy table models
core          : Store config, security, dependencies, and permissions
constants     : Store role and status constants
utils         : Store reusable helpers
```

## Project Structure

```txt
student-counseling-api/
├── app/
│   ├── core/
│   ├── constants/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   └── main.py
├── docs/
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── AGENTS.md
├── alembic.ini
├── README.md
└── requirements.txt
```

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
APP_NAME="Student Counseling API"
APP_ENV="development"
APP_VERSION="0.1.0"

DATABASE_URL="postgresql+psycopg2://postgres:your_password@localhost:5432/student_counseling_db"
TEST_DATABASE_URL="postgresql+psycopg2://postgres:your_password@localhost:5432/student_counseling_test_db"

JWT_SECRET_KEY="change-this-secret-key"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

Important notes:

* Do not commit `.env`
* Use `.env.example` for safe configuration examples
* Use a strong `JWT_SECRET_KEY` in real environments
* Use a separate test database for automated testing

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd student-counseling-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Create PostgreSQL databases:

```sql
CREATE DATABASE student_counseling_db;
CREATE DATABASE student_counseling_test_db;
```

Run Alembic migrations:

```bash
alembic upgrade head
```

## Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```txt
http://127.0.0.1:8000
```

## Running with Docker

Build the Docker image:

```bash
docker build -t student-counseling-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 --name student-counseling-api student-counseling-api
```

The API will be available at:

```txt
http://127.0.0.1:8000
```

Test the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Notes:

* The current Docker setup runs the FastAPI application container only.
* Database endpoints require a PostgreSQL database connection.
* Docker Compose with PostgreSQL will be added in a future improvement.

## Running with Docker Compose

This project also supports Docker Compose for running the FastAPI application together with a PostgreSQL database.

Build and start the services:

```bash
docker compose up --build
```

The API will be available at:

```txt
http://127.0.0.1:8000
```

The PostgreSQL database container uses the following local port mapping:

```txt
localhost:5434 -> container:5432
```

Test the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Stop the services:

```bash
docker compose down
```

Remove containers and volumes if you want to reset the database:

```bash
docker compose down -v
```

Notes:

* The API service runs Alembic migrations automatically before starting the FastAPI server.
* The database service uses PostgreSQL 16 Alpine.
* The API connects to PostgreSQL through Docker internal networking using `db:5432`.
* The exposed PostgreSQL host port is `5434` to avoid conflict with a local PostgreSQL installation.


## API Documentation

FastAPI automatically provides interactive API documentation:

```txt
http://127.0.0.1:8000/docs
```

Health check endpoint:

```txt
GET /health
```

## API Modules

Main API modules:

```txt
/auth
/students
/counseling-records
/assessments
/reports
```

## Testing

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Current test coverage includes:

* Health endpoint
* Authentication
* Role authorization
* Student CRUD
* Counseling Records CRUD
* Assessments CRUD
* Reports Summary

Current test status:

```txt
35 passed
```

## Security Notes

Implemented security features:

* Password hashing with bcrypt
* JWT authentication
* Protected routes
* Role-based authorization
* Environment variable configuration
* Separate development and test databases
* `.env` excluded from Git

## Development Status

Current phase:

```txt
Phase 11 - Portfolio Polish
```

Completed:

* FastAPI basic setup
* PostgreSQL database connection
* SQLAlchemy models
* Alembic migrations
* JWT authentication
* Role-based authorization
* Student CRUD
* Counseling Records CRUD
* Assessments CRUD
* Reports Summary
* Automated testing
* Environment example file
* Git ignore rules
* Requirements file
* Dockerfile and basic Docker image support
* Docker Compose setup with PostgreSQL

Next planned improvements:

* More pagination and filtering improvements
* API response consistency improvements
* Deployment preparation
* CI testing workflow
* Production-ready Docker configuration improvements
* CI testing workflow
* Deployment preparation


## Portfolio Notes

This project is designed to show backend development fundamentals in a realistic school counseling API domain.

The codebase focuses on:

* Clean architecture
* Maintainable structure
* Clear business rules
* Secure authentication flow
* Database migration discipline
* Automated testing
* Portfolio-ready documentation

## License

This project is created for learning and portfolio purposes.
