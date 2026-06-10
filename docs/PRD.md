# PRD — Student Counseling Backend API

## 1. Project Overview

Student Counseling Backend API adalah backend system untuk membantu sekolah mengelola data siswa, catatan konseling, kotak curhat, dan laporan dasar bimbingan konseling.

Project ini dibuat sebagai backend API menggunakan FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT Authentication, Role-Based Authorization, dan automated testing dasar.

Fokus utama project ini adalah membangun backend yang rapi, aman, mudah dirawat, dan layak digunakan sebagai portfolio Junior Backend Developer Python.

---

## 2. Goals

Tujuan project:

1. Membuat REST API backend yang rapi dan profesional.
2. Mengelola data siswa dengan pagination, search, dan filter.
3. Mengelola catatan konseling siswa.
4. Menyediakan fitur kotak curhat untuk siswa.
5. Membuat sistem login dan register menggunakan JWT.
6. Membuat role-based access control.
7. Menyediakan laporan aggregate untuk guru BK, admin, dan kepala sekolah.
8. Melatih struktur backend yang bersih: route, service, repository, schema, model.
9. Melatih debugging, testing, dan deployment backend.

---

## 3. Non-Goals

Fitur berikut tidak termasuk MVP:

1. Frontend Next.js.
2. File upload.
3. Export PDF.
4. Import Excel.
5. WhatsApp integration.
6. AI analysis.
7. Real-time chat.
8. Multi-school / multi-tenant system.
9. Payment system.
10. Mobile app.

Fitur tersebut bisa menjadi future enhancement setelah MVP selesai.

---

## 4. Target Users

### 4.1 Admin

Admin bertugas mengelola user dan data master.

Admin dapat:

- Mengelola user.
- Mengelola data siswa.
- Mengakses catatan konseling.
- Mengakses kotak curhat.
- Melihat laporan aggregate.

### 4.2 Counselor

Counselor adalah guru BK.

Counselor dapat:

- Mengelola data siswa.
- Mengelola catatan konseling.
- Melihat dan menangani kotak curhat.
- Melihat laporan aggregate.

### 4.3 Student

Student adalah siswa.

Student dapat:

- Login ke sistem.
- Mengirim curhat.
- Melihat curhat miliknya sendiri.
- Melihat status dan response curhat miliknya sendiri.

Student tidak boleh melihat data siswa lain, catatan konseling, atau laporan sekolah.

### 4.4 Principal

Principal adalah kepala sekolah.

Principal dapat:

- Melihat laporan aggregate.
- Tidak boleh melihat isi detail curhat.
- Tidak boleh melihat detail sensitif catatan konseling.
- Tidak boleh mengubah data siswa.

---

## 5. MVP Features

### 5.1 Authentication

Fitur:

- Register user.
- Login user.
- Generate JWT token.
- Get current user.
- Protected endpoint.

Endpoint:

- POST /auth/register
- POST /auth/login
- GET /auth/me

---

### 5.2 User Management

Fitur:

- Admin dapat membuat user.
- Admin dapat melihat daftar user.
- Admin dapat melihat detail user.
- Admin dapat mengubah data user.
- Admin dapat menonaktifkan user.

Endpoint:

- GET /users
- GET /users/{id}
- POST /users
- PATCH /users/{id}
- DELETE /users/{id}

---

### 5.3 Student Management

Fitur:

- Admin dan counselor dapat menambah siswa.
- Admin dan counselor dapat melihat daftar siswa.
- Admin dan counselor dapat mencari siswa berdasarkan nama.
- Admin dan counselor dapat filter siswa berdasarkan kelas, jurusan, status, dan tahun ajaran.
- Admin dan counselor dapat melihat detail siswa.
- Admin dan counselor dapat mengubah data siswa.
- Admin dapat menghapus atau menonaktifkan data siswa.

Endpoint:

- GET /students
- GET /students/{id}
- POST /students
- PATCH /students/{id}
- DELETE /students/{id}

Query:

- page
- limit
- search
- class_name
- major
- academic_year
- status

Example:

```txt
GET /students?page=1&limit=10&search=budi&class_name=XII&major=TKJ
```

---

### 5.4 Counseling Records

Fitur:

- Admin dan counselor dapat membuat catatan konseling.
- Admin dan counselor dapat melihat catatan konseling.
- Admin dan counselor dapat filter catatan berdasarkan siswa, kategori, dan tanggal.
- Admin dan counselor dapat mengubah catatan konseling.
- Admin dapat menghapus catatan konseling.

Endpoint:

- GET /counseling-records
- GET /counseling-records/{id}
- POST /counseling-records
- PATCH /counseling-records/{id}
- DELETE /counseling-records/{id}

---

### 5.5 Confession Box

Fitur:

- Student dapat membuat curhat.
- Student hanya dapat melihat curhat miliknya sendiri.
- Counselor dapat melihat semua curhat.
- Counselor dapat mengubah status curhat.
- Counselor dapat memberi response terhadap curhat.
- Admin dapat melihat semua curhat.
- Principal tidak dapat melihat detail curhat.

Endpoint:

- GET /confessions
- GET /confessions/{id}
- POST /confessions
- PATCH /confessions/{id}/status
- PATCH /confessions/{id}/response

Status:

- pending
- in_review
- resolved
- rejected

---

### 5.6 Reports

Fitur:

- Jumlah siswa.
- Jumlah siswa per kelas.
- Jumlah catatan konseling bulan ini.
- Jumlah curhat berdasarkan status.
- Jumlah konseling per bulan.
- Jumlah curhat per bulan.

Endpoint:

- GET /reports/summary
- GET /reports/students-by-class
- GET /reports/counseling-by-month
- GET /reports/confession-status

Rules:

- Admin dapat melihat laporan.
- Counselor dapat melihat laporan.
- Principal dapat melihat laporan aggregate.
- Student tidak dapat melihat laporan.

---

## 6. Role Access Matrix

| Feature | Admin | Counselor | Student | Principal |
|---|---:|---:|---:|---:|
| Register | Yes | No | No | No |
| Login | Yes | Yes | Yes | Yes |
| Manage Users | Yes | No | No | No |
| View Students | Yes | Yes | No | Aggregate only |
| Create Student | Yes | Yes | No | No |
| Update Student | Yes | Yes | No | No |
| Delete Student | Yes | No | No | No |
| View Counseling Records | Yes | Yes | No | Aggregate only |
| Create Counseling Record | Yes | Yes | No | No |
| Update Counseling Record | Yes | Yes | No | No |
| Delete Counseling Record | Yes | No | No | No |
| Create Confession | No | No | Own only | No |
| View Confession Detail | Yes | Yes | Own only | No |
| Update Confession Status | Yes | Yes | No | No |
| View Reports | Yes | Yes | No | Yes |

---

## 7. Success Criteria

Project dianggap selesai MVP jika:

1. FastAPI backend dapat berjalan secara lokal.
2. PostgreSQL berhasil terkoneksi.
3. Alembic migration berjalan.
4. Register dan login berjalan.
5. Password disimpan dalam bentuk hash.
6. JWT token dapat digunakan untuk protected endpoint.
7. Role authorization berjalan.
8. CRUD students berjalan.
9. CRUD counseling records berjalan.
10. Confession box berjalan sesuai role.
11. Reports aggregate berjalan.
12. Pagination, search, dan filter berjalan.
13. Error handling jelas.
14. Basic testing tersedia.
15. README menjelaskan setup, env, run, test, dan deployment.
16. Tidak ada secret atau API key di repository.

---

## 8. Future Enhancements

Fitur lanjutan setelah MVP:

1. Frontend dashboard.
2. Export PDF.
3. Import Excel.
4. Upload dokumen.
5. Notification.
6. WhatsApp integration.
7. AI summary untuk catatan konseling.
8. Multi-school support.
9. Audit log.
10. Advanced reporting.
