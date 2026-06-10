import uuid

from fastapi.testclient import TestClient

from tests.helpers import get_auth_headers


def _unique_nis() -> str:
    unique_id = uuid.uuid4().hex[:8]
    return f"NIS{unique_id}"


def _build_student_payload() -> dict:
    return {
        "nis": _unique_nis(),
        "name": "Test Student",
        "gender": "male",
        "class_name": "XII RPL 1",
        "major": "Software Engineering",
        "academic_year": "2025/2026",
        "phone": "081234567890",
        "address": "Test Address",
        "status": "active",
    }

def _extract_student_data(response_json: dict) -> dict:
    if "data" in response_json and isinstance(response_json["data"], dict):
        return response_json["data"]

    return response_json

def _create_student(
    client: TestClient,
    *,
    headers: dict[str, str],
) -> dict:
    payload = _build_student_payload()

    response = client.post(
        "/students",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201, response.json()

    return _extract_student_data(response.json())


def test_admin_can_create_student(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="admin")
    payload = _build_student_payload()

    response = client.post(
        "/students",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201, response.json()

    data = _extract_student_data(response.json())

    assert data["nis"] == payload["nis"]
    assert data["name"] == payload["name"]
    assert data["gender"] == payload["gender"]
    assert data["class_name"] == payload["class_name"]
    assert data["major"] == payload["major"]
    assert data["academic_year"] == payload["academic_year"]
    assert data["status"] == payload["status"]


def test_admin_can_list_students(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="admin")

    _create_student(client=client, headers=headers)

    response = client.get(
        "/students",
        headers=headers,
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 1

def test_admin_can_get_student_detail(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="admin")

    created_student = _create_student(client=client, headers=headers)
    student_id = created_student["id"]

    response = client.get(
        f"/students/{student_id}",
        headers=headers,
    )

    assert response.status_code == 200, response.json()

    data = _extract_student_data(response.json())

    assert data["id"] == student_id
    assert data["nis"] == created_student["nis"]
    assert data["name"] == created_student["name"]

def test_admin_can_update_student(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="admin")

    created_student = _create_student(client=client, headers=headers)
    student_id = created_student["id"]

    response = client.patch(
        f"/students/{student_id}",
        json={
            "name": "Updated Student",
            "class_name": "XI RPL 2",
        },
        headers=headers,
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["id"] == student_id
    assert data["name"] == "Updated Student"
    assert data["class_name"] == "XI RPL 2"


def test_admin_can_delete_student(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="admin")

    created_student = _create_student(client=client, headers=headers)
    student_id = created_student["id"]

    response = client.delete(
        f"/students/{student_id}",
        headers=headers,
    )

    assert response.status_code == 204


def test_counselor_cannot_delete_student(client: TestClient) -> None:
    admin_headers = get_auth_headers(client=client, role="admin")
    counselor_headers = get_auth_headers(client=client, role="counselor")

    created_student = _create_student(client=client, headers=admin_headers)
    student_id = created_student["id"]

    response = client.delete(
        f"/students/{student_id}",
        headers=counselor_headers,
    )

    assert response.status_code == 403


def test_student_cannot_access_students(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="student")

    response = client.get(
        "/students",
        headers=headers,
    )

    assert response.status_code == 403


def test_principal_cannot_access_students(client: TestClient) -> None:
    headers = get_auth_headers(client=client, role="principal")

    response = client.get(
        "/students",
        headers=headers,
    )

    assert response.status_code == 403