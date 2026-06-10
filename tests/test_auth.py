import uuid

from fastapi.testclient import TestClient


TEST_PASSWORD = "Password123!"


def _unique_email(prefix: str = "user") -> str:
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{unique_id}@example.com"


def _build_register_payload(
    *,
    email: str,
    role: str = "counselor",
) -> dict:
    return {
        "name": "Test User",
        "email": email,
        "password": TEST_PASSWORD,
        "role": role,
    }


def _register_user(
    client: TestClient,
    *,
    email: str,
    role: str = "counselor",
):
    return client.post(
        "/auth/register",
        json=_build_register_payload(
            email=email,
            role=role,
        ),
    )


def _login_user(
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


def test_register_user_success(client: TestClient) -> None:
    email = _unique_email("register")

    response = _register_user(
        client=client,
        email=email,
        role="counselor",
    )

    assert response.status_code == 201, response.json()

    data = response.json()

    assert data["email"] == email
    assert data["role"] == "counselor"
    assert "password" not in data
    assert "hashed_password" not in data

def test_login_user_success(client: TestClient) -> None:
    email = _unique_email("login")

    register_response = _register_user(
        client=client,
        email=email,
        role="counselor",
    )

    assert register_response.status_code == 201

    login_response = _login_user(
        client=client,
        email=email,
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_get_current_user_success(client: TestClient) -> None:
    email = _unique_email("me")

    register_response = _register_user(
        client=client,
        email=email,
        role="counselor",
    )

    assert register_response.status_code == 201

    login_response = _login_user(
        client=client,
        email=email,
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["email"] == email
    assert data["role"] == "counselor"
    assert "password" not in data
    assert "hashed_password" not in data


def test_get_current_user_without_token_fails(client: TestClient) -> None:
    response = client.get("/auth/me")

    assert response.status_code in {401, 403}