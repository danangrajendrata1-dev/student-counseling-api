# Database Schema — Student Counseling Backend API

## 1. Tables Overview

MVP menggunakan tabel:

1. users
2. students
3. counseling_records
4. confessions

---

## 2. users

Menyimpan data akun pengguna.

| Column | Type | Constraint |
|---|---|---|
| id | UUID | Primary Key |
| name | VARCHAR(150) | Not Null |
| email | VARCHAR(255) | Unique, Not Null |
| hashed_password | VARCHAR(255) | Not Null |
| role | VARCHAR(30) | Not Null |
| is_active | BOOLEAN | Default True |
| created_at | TIMESTAMP | Not Null |
| updated_at | TIMESTAMP | Not Null |

Allowed role:

```txt
admin
counselor
student
principal
```

---

## 3. students

Menyimpan data siswa.

| Column | Type | Constraint |
|---|---|---|
| id | UUID | Primary Key |
| user_id | UUID | Foreign Key users.id, Nullable |
| nis | VARCHAR(50) | Unique, Not Null |
| name | VARCHAR(150) | Not Null |
| gender | VARCHAR(20) | Not Null |
| class_name | VARCHAR(50) | Not Null |
| major | VARCHAR(100) | Nullable |
| academic_year | VARCHAR(20) | Not Null |
| phone | VARCHAR(30) | Nullable |
| address | TEXT | Nullable |
| status | VARCHAR(30) | Not Null |
| created_at | TIMESTAMP | Not Null |
| updated_at | TIMESTAMP | Not Null |

Allowed status:

```txt
active
inactive
graduated
transferred
```

---

## 4. counseling_records

Menyimpan catatan konseling siswa.

| Column | Type | Constraint |
|---|---|---|
| id | UUID | Primary Key |
| student_id | UUID | Foreign Key students.id, Not Null |
| counselor_id | UUID | Foreign Key users.id, Not Null |
| case_title | VARCHAR(200) | Not Null |
| case_category | VARCHAR(100) | Not Null |
| description | TEXT | Not Null |
| action_taken | TEXT | Nullable |
| follow_up_plan | TEXT | Nullable |
| counseling_date | DATE | Not Null |
| created_at | TIMESTAMP | Not Null |
| updated_at | TIMESTAMP | Not Null |

---

## 5. confessions

Menyimpan pesan kotak curhat siswa.

| Column | Type | Constraint |
|---|---|---|
| id | UUID | Primary Key |
| student_id | UUID | Foreign Key students.id, Not Null |
| title | VARCHAR(200) | Not Null |
| message | TEXT | Not Null |
| status | VARCHAR(30) | Not Null |
| response | TEXT | Nullable |
| handled_by | UUID | Foreign Key users.id, Nullable |
| created_at | TIMESTAMP | Not Null |
| updated_at | TIMESTAMP | Not Null |

Allowed status:

```txt
pending
in_review
resolved
rejected
```

---

## 6. Suggested Indexes

users:

```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

students:

```sql
CREATE INDEX idx_students_name ON students(name);
CREATE INDEX idx_students_class_name ON students(class_name);
CREATE INDEX idx_students_major ON students(major);
CREATE INDEX idx_students_academic_year ON students(academic_year);
CREATE INDEX idx_students_status ON students(status);
```

counseling_records:

```sql
CREATE INDEX idx_counseling_records_student_id ON counseling_records(student_id);
CREATE INDEX idx_counseling_records_counselor_id ON counseling_records(counselor_id);
CREATE INDEX idx_counseling_records_counseling_date ON counseling_records(counseling_date);
CREATE INDEX idx_counseling_records_case_category ON counseling_records(case_category);
```

confessions:

```sql
CREATE INDEX idx_confessions_student_id ON confessions(student_id);
CREATE INDEX idx_confessions_status ON confessions(status);
CREATE INDEX idx_confessions_handled_by ON confessions(handled_by);
```

---

## 7. Relationships

```txt
users 1 ── 0..1 students
students 1 ── many counseling_records
users 1 ── many counseling_records as counselor
students 1 ── many confessions
users 1 ── many confessions as handler
```

---

## 8. Data Privacy Rules

1. Student tidak boleh melihat data siswa lain.
2. Student tidak boleh melihat catatan konseling.
3. Student hanya boleh melihat confession miliknya sendiri.
4. Principal hanya boleh melihat data aggregate.
5. Confession detail tidak boleh dibuka oleh principal.
6. Counseling record detail hanya boleh diakses admin dan counselor.
