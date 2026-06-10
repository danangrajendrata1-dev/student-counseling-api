# Technical Design — Student Counseling Backend API

## 1. Tech Stack

Backend:

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- JWT
- Passlib / bcrypt
- Pytest

Development tools:

- Uvicorn
- python-dotenv / pydantic-settings
- Docker
- GitHub

---

## 2. Architecture Pattern

Project menggunakan layered architecture:

```txt
Route → Service → Repository → Database
```

Penjelasan:

- Route menerima HTTP request dan mengembalikan HTTP response.
- Schema melakukan validasi request dan response.
- Service menyimpan business logic.
- Repository bertanggung jawab terhadap query database.
- Model merepresentasikan tabel database.
- Core menyimpan config, security, dan permission.
- Utils menyimpan helper umum seperti pagination dan response format.

---

## 3. Folder Structure

```txt
student-counseling-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── permissions.py
│   ├── models/
│   │   ├── user_model.py
│   │   ├── student_model.py
│   │   ├── counseling_record_model.py
│   │   └── confession_model.py
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── student_schema.py
│   │   ├── counseling_record_schema.py
│   │   └── confession_schema.py
│   ├── routes/
│   │   ├── auth_route.py
│   │   ├── user_route.py
│   │   ├── student_route.py
│   │   ├── counseling_record_route.py
│   │   ├── confession_route.py
│   │   └── report_route.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── student_repository.py
│   │   ├── counseling_record_repository.py
│   │   └── confession_repository.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── student_service.py
│   │   ├── counseling_record_service.py
│   │   ├── confession_service.py
│   │   └── report_service.py
│   └── utils/
│       ├── pagination.py
│       └── response.py
├── docs/
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 4. API Response Format

Response sukses:

```json
{
  "message": "Students fetched successfully",
  "data": []
}
```

Response dengan pagination:

```json
{
  "message": "Students fetched successfully",
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "total_pages": 10
  }
}
```

Response error:

```json
{
  "detail": "Student not found"
}
```

---

## 5. Authentication Flow

1. User mengirim email dan password ke endpoint login.
2. Backend mengecek user berdasarkan email.
3. Backend memverifikasi password menggunakan bcrypt.
4. Jika valid, backend membuat JWT access token.
5. Client menggunakan token pada header Authorization.

Format header:

```txt
Authorization: Bearer <token>
```

---

## 6. Authorization Flow

Setiap protected endpoint akan memeriksa:

1. Apakah user sudah login.
2. Apakah token valid.
3. Apakah user aktif.
4. Apakah role user diperbolehkan mengakses endpoint tersebut.

Contoh:

- /users hanya admin.
- /students admin dan counselor.
- /reports admin, counselor, principal.
- /confessions student hanya miliknya sendiri.

---

## 7. Database Access Pattern

Route tidak boleh langsung query database.

Benar:

```txt
route → service → repository → database
```

Salah:

```txt
route → database langsung
```

Repository hanya berisi query database.

Service berisi business logic, validasi, dan permission tambahan.

---

## 8. Pagination Strategy

Endpoint list wajib menggunakan pagination.

Default:

```txt
page = 1
limit = 10
max_limit = 100
```

Formula offset:

```txt
offset = (page - 1) * limit
```

---

## 9. Error Handling Strategy

Gunakan HTTPException untuk error yang diprediksi.

Contoh:

- 400 Bad Request untuk input salah.
- 401 Unauthorized untuk belum login.
- 403 Forbidden untuk akses ditolak.
- 404 Not Found untuk data tidak ditemukan.
- 409 Conflict untuk data duplikat.
- 500 Internal Server Error untuk error tidak terduga.

---

## 10. Testing Strategy

Testing minimal:

- Auth register.
- Auth login.
- Auth wrong password.
- Protected endpoint without token.
- Admin create student.
- Counselor create counseling record.
- Student create confession.
- Student cannot view other student confession.
- Principal can access aggregate reports.
- Principal cannot access confession detail.

---

## 11. Deployment Strategy

Local development:

```txt
FastAPI + PostgreSQL local
```

Production options:

```txt
Backend: Render / Google Cloud Run
Database: Neon / Supabase PostgreSQL
```

Configuration wajib menggunakan environment variable.

Tidak boleh hardcode database URL, JWT secret, atau production URL.
