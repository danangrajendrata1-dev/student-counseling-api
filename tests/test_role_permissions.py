from fastapi.testclient import TestClient

from tests.helpers import get_auth_headers


def test_admin_can_access_all_debug_permission_endpoints(
    client: TestClient,
) -> None:
    headers = get_auth_headers(client=client, role="admin")

    admin_only_response = client.get(
        "/debug/permissions/admin-only",
        headers=headers,
    )
    admin_or_counselor_response = client.get(
        "/debug/permissions/admin-or-counselor",
        headers=headers,
    )
    report_access_response = client.get(
        "/debug/permissions/report-access",
        headers=headers,
    )

    assert admin_only_response.status_code == 200
    assert admin_or_counselor_response.status_code == 200
    assert report_access_response.status_code == 200


def test_counselor_can_access_allowed_debug_permission_endpoints(
    client: TestClient,
) -> None:
    headers = get_auth_headers(client=client, role="counselor")

    admin_only_response = client.get(
        "/debug/permissions/admin-only",
        headers=headers,
    )
    admin_or_counselor_response = client.get(
        "/debug/permissions/admin-or-counselor",
        headers=headers,
    )
    report_access_response = client.get(
        "/debug/permissions/report-access",
        headers=headers,
    )

    assert admin_only_response.status_code == 403
    assert admin_or_counselor_response.status_code == 200
    assert report_access_response.status_code == 200


def test_student_cannot_access_debug_permission_endpoints(
    client: TestClient,
) -> None:
    headers = get_auth_headers(client=client, role="student")

    admin_only_response = client.get(
        "/debug/permissions/admin-only",
        headers=headers,
    )
    admin_or_counselor_response = client.get(
        "/debug/permissions/admin-or-counselor",
        headers=headers,
    )
    report_access_response = client.get(
        "/debug/permissions/report-access",
        headers=headers,
    )

    assert admin_only_response.status_code == 403
    assert admin_or_counselor_response.status_code == 403
    assert report_access_response.status_code == 403


def test_principal_can_only_access_report_debug_permission_endpoint(
    client: TestClient,
) -> None:
    headers = get_auth_headers(client=client, role="principal")

    admin_only_response = client.get(
        "/debug/permissions/admin-only",
        headers=headers,
    )
    admin_or_counselor_response = client.get(
        "/debug/permissions/admin-or-counselor",
        headers=headers,
    )
    report_access_response = client.get(
        "/debug/permissions/report-access",
        headers=headers,
    )

    assert admin_only_response.status_code == 403
    assert admin_or_counselor_response.status_code == 403
    assert report_access_response.status_code == 200