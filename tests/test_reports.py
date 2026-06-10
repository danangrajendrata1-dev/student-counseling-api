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


def _build_assessment_payload(student_id) -> dict:
    return {
        "student_id": student_id,
        "assessment_type": "learning_style",
        "assessment_date": "2026-06-10",
        "score": 85,
        "result": "Visual learner",
        "notes": "Siswa lebih mudah memahami materi melalui gambar dan diagram.",
    }


def _create_assessment(
    client: TestClient,
    *,
    headers: dict[str, str],
    student_id,
) -> dict:
    response = client.post(
        "/assessments",
        json=_build_assessment_payload(student_id),
        headers=headers,
    )

    assert response.status_code == 201, response.json()

    return response.json()


def test_admin_can_get_report_summary_and_counts_increase(
    client: TestClient,
) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    before_response = client.get(
        "/reports/summary",
        headers=admin_headers,
    )

    assert before_response.status_code == 200, before_response.json()

    before = before_response.json()

    student = create_student(client=client, headers=admin_headers)

    _create_counseling_record(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    _create_assessment(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    after_response = client.get(
        "/reports/summary",
        headers=admin_headers,
    )

    assert after_response.status_code == 200, after_response.json()

    after = after_response.json()

    assert after["total_students"] == before["total_students"] + 1
    assert after["active_students"] == before["active_students"] + 1
    assert after["total_counseling_records"] == before["total_counseling_records"] + 1
    assert after["open_counseling_records"] == before["open_counseling_records"] + 1
    assert after["total_assessments"] == before["total_assessments"] + 1

    assert "counseling_records_by_status" in after
    assert "assessments_by_type" in after
    assert after["counseling_records_by_status"]["open"] >= 1
    assert after["assessments_by_type"]["learning_style"] >= 1


def test_counselor_can_get_report_summary(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="counselor")

    response = client.get(
        "/reports/summary",
        headers=headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert "total_students" in data
    assert "total_counseling_records" in data
    assert "total_assessments" in data


def test_principal_can_get_report_summary(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="principal")

    response = client.get(
        "/reports/summary",
        headers=headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert "total_students" in data
    assert "total_counseling_records" in data
    assert "total_assessments" in data


def test_student_cannot_get_report_summary(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="student")

    response = client.get(
        "/reports/summary",
        headers=headers,
    )

    assert response.status_code == 403