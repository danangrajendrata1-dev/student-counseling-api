from fastapi.testclient import TestClient

from tests.helpers import create_student, get_auth_headers


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


def test_counselor_can_create_assessment(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)

    response = client.post(
        "/assessments",
        json=_build_assessment_payload(student["id"]),
        headers=counselor_headers,
    )

    assert response.status_code == 201, response.json()

    data = response.json()

    assert data["student_id"] == student["id"]
    assert data["assessment_type"] == "learning_style"
    assert data["score"] == 85
    assert data["result"] == "Visual learner"
    assert "created_by" in data


def test_counselor_can_list_assessments(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    _create_assessment(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.get(
        "/assessments",
        headers=counselor_headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert "data" in data
    assert "meta" in data
    assert isinstance(data["data"], list)
    assert data["meta"]["total"] >= 1


def test_counselor_can_get_assessment_detail(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    assessment = _create_assessment(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.get(
        f"/assessments/{assessment['id']}",
        headers=counselor_headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert "data" in data
    assert data["data"]["id"] == assessment["id"]
    assert data["data"]["student_id"] == student["id"]


def test_counselor_can_update_assessment(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    assessment = _create_assessment(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.patch(
        f"/assessments/{assessment['id']}",
        json={
            "score": 90,
            "result": "Visual-dominant learner",
            "notes": "Siswa sangat terbantu dengan diagram, mind map, dan ilustrasi.",
        },
        headers=counselor_headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["id"] == assessment["id"]
    assert data["score"] == 90
    assert data["result"] == "Visual-dominant learner"


def test_admin_can_delete_assessment(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    student = create_student(client=client, headers=admin_headers)
    assessment = _create_assessment(
        client=client,
        headers=counselor_headers,
        student_id=student["id"],
    )

    response = client.delete(
        f"/assessments/{assessment['id']}",
        headers=admin_headers,
    )

    assert response.status_code == 204


def test_student_cannot_access_assessments(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="student")

    response = client.get(
        "/assessments",
        headers=headers,
    )

    assert response.status_code == 403


def test_principal_cannot_access_assessments(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="principal")

    response = client.get(
        "/assessments",
        headers=headers,
    )

    assert response.status_code == 403