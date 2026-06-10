# Security Rules — Student Counseling Backend API

## 1. Authentication

1. Semua endpoint sensitif harus protected.
2. Password tidak boleh disimpan dalam bentuk plain text.
3. Password wajib di-hash menggunakan bcrypt.
4. JWT token tidak boleh menyimpan password.
5. JWT token minimal menyimpan user_id dan role.
6. JWT secret wajib disimpan di environment variable.
7. Token expiration wajib digunakan.

---

## 2. Authorization

Role yang digunakan:

```txt
admin
counselor
student
principal
```

Aturan umum:

1. Admin dapat mengelola semua data.
2. Counselor dapat mengelola data siswa, counseling records, dan confessions.
3. Student hanya dapat mengakses data miliknya sendiri.
4. Principal hanya dapat mengakses laporan aggregate.
5. Principal tidak boleh mengakses detail confession.
6. Principal tidak boleh mengakses detail counseling records.

---

## 3. Data Privacy

Data sensitif:

1. Counseling record description.
2. Action taken.
3. Follow up plan.
4. Confession message.
5. Confession response.
6. Student personal information.

Aturan:

1. Jangan return data sensitif ke role yang tidak berhak.
2. Jangan expose hashed_password di response API.
3. Jangan expose internal error detail ke client.
4. Jangan log password atau token.
5. Student tidak boleh melihat confession milik student lain.
6. Student tidak boleh melihat counseling records.

---

## 4. Input Validation

Semua request body wajib divalidasi menggunakan Pydantic schema.

Validasi minimal:

1. Email harus valid.
2. Password minimal 8 karakter.
3. Name tidak boleh kosong.
4. NIS tidak boleh kosong.
5. Role harus salah satu dari allowed role.
6. Status harus salah satu dari allowed status.
7. Pagination limit maksimal 100.
8. Search query harus dibatasi panjangnya.

---

## 5. Database Security

1. Database URL wajib disimpan di .env.
2. Jangan commit .env ke GitHub.
3. Gunakan unique constraint untuk email dan NIS.
4. Gunakan foreign key untuk relasi penting.
5. Gunakan transaction untuk operasi yang saling bergantung.
6. Gunakan migration untuk perubahan schema.

---

## 6. Error Handling

Gunakan status code yang sesuai:

```txt
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
500 Internal Server Error
```

Aturan:

1. Jangan return traceback ke client.
2. Error message harus jelas tapi tidak membocorkan detail internal.
3. Duplicate email harus return 409 Conflict.
4. Invalid login harus return 401 Unauthorized.
5. Role tidak berhak harus return 403 Forbidden.

---

## 7. Environment Variables

Environment variables minimal:

```txt
APP_NAME
APP_ENV
DATABASE_URL
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
CORS_ORIGINS
```

Aturan:

1. Semua secret disimpan di .env.
2. .env tidak boleh masuk GitHub.
3. .env.example wajib disediakan.
4. Production secret harus berbeda dari development secret.

---

## 8. CORS

1. CORS development boleh mengizinkan localhost.
2. CORS production hanya boleh mengizinkan domain frontend resmi.
3. Jangan gunakan wildcard "*" di production.

---

## 9. Testing Security

Minimal test security:

1. User tanpa token tidak bisa akses protected endpoint.
2. Student tidak bisa akses data siswa lain.
3. Principal tidak bisa akses confession detail.
4. Counselor bisa melihat confessions.
5. Admin bisa create user.
6. Password tidak muncul di response.
7. Login dengan password salah gagal.
