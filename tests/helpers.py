import uuid

from fastapi.testclient import TestClient


TEST_PASSWORD = "Password123!"


def unique_email(prefix: str = "user") -> str:
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{unique_id}@example.com"


def build_register_payload(
    *,
    email: str,
    role: str,
) -> dict:
    return {
        "name": "Test User",
        "email": email,
        "password": TEST_PASSWORD,
        "role": role,
    }


def register_user(
    client: TestClient,
    *,
    role: str,
):
    email = unique_email(role)

    response = client.post(
        "/auth/register",
        json=build_register_payload(
            email=email,
            role=role,
        ),
    )

    return response, email


def login_user(
    client: TestClient,
    *,
    email: str,
):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": TEST_PASSWORD,
        },
    )


def get_auth_headers(
    client: TestClient,
    *,
    role: str,
) -> dict[str, str]:
    register_response, email = register_user(
        client=client,
        role=role,
    )

    assert register_response.status_code == 201, register_response.json()

    login_response = login_user(
        client=client,
        email=email,
    )

    assert login_response.status_code == 200, login_response.json()

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }

def unique_nis() -> str:
    unique_id = uuid.uuid4().hex[:8]
    return f"NIS{unique_id}"


def extract_response_data(response_json: dict) -> dict:
    if "data" in response_json and isinstance(response_json["data"], dict):
        return response_json["data"]

    return response_json


def build_student_payload() -> dict:
    return {
        "nis": unique_nis(),
        "name": "Test Student",
        "gender": "male",
        "class_name": "XII RPL 1",
        "major": "Software Engineering",
        "academic_year": "2025/2026",
        "phone": "081234567890",
        "address": "Test Address",
        "status": "active",
    }


def create_student(
    client: TestClient,
    *,
    headers: dict[str, str],
) -> dict:
    response = client.post(
        "/students",
        json=build_student_payload(),
        headers=headers,
    )

    assert response.status_code == 201, response.json()

    return extract_response_data(response.json())