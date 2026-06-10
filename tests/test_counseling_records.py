from fastapi.testclient import TestClient

from tests.helpers import create_student, get_auth_headers


def _build_counseling_record_payload(student_id) -> dict:
    return {
        "student_id": student_id,
        "counseling_date": "2026-06-10",
        "topic": "Kesulitan belajar matematika",
        "description": "Siswa mengalami kesulitan memahami materi aljabar.",
        "follow_up": "Jadwalkan sesi konseling lanjutan minggu depan.",
        "status": "open",
    }


def _create_counseling_record(
    client: TestClient,
    *,
    headers: dict[str, str],
    student_id,
) -> dict:
    response = client.post(
        "/counseling-records",
        json=_build_counseling_record_payload(student_id),
        headers=headers,
    )

    assert response.status_code == 201, response.json()

    return response.json()


def test_counselor_can_create_counseling_record(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)

    response = client.post(
        "/counseling-records",
        json=_build_counseling_record_payload(student["id"]),
        headers=counselor_headers,
    )

    assert response.status_code == 201, response.json()

    data = response.json()

    assert data["student_id"] == student["id"]
    assert data["topic"] == "Kesulitan belajar matematika"
    assert data["status"] == "open"
    assert "counselor_id" in data


def test_counselor_can_list_counseling_records(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    _create_counseling_record(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.get(
        "/counseling-records",
        headers=counselor_headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert "data" in data
    assert "meta" in data
    assert isinstance(data["data"], list)
    assert data["meta"]["total"] >= 1


def test_counselor_can_get_counseling_record_detail(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    record = _create_counseling_record(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.get(
        f"/counseling-records/{record['id']}",
        headers=counselor_headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert "data" in data
    assert data["data"]["id"] == record["id"]
    assert data["data"]["student_id"] == student["id"]


def test_counselor_can_update_counseling_record(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    record = _create_counseling_record(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.patch(
        f"/counseling-records/{record['id']}",
        json={
            "status": "in_progress",
            "follow_up": "Koordinasi dengan wali kelas.",
        },
        headers=counselor_headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["id"] == record["id"]
    assert data["status"] == "in_progress"
    assert data["follow_up"] == "Koordinasi dengan wali kelas."


def test_admin_can_delete_counseling_record(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    record = _create_counseling_record(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.delete(
        f"/counseling-records/{record['id']}",
        headers=admin_headers,
    )

    assert response.status_code == 204


def test_student_cannot_access_counseling_records(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="student")

    response = client.get(
        "/counseling-records",
        headers=headers,
    )

    assert response.status_code == 403


def test_principal_cannot_access_counseling_records(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="principal")

    response = client.get(
        "/counseling-records",
        headers=headers,
    )

    assert response.status_code == 403