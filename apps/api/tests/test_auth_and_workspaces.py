from __future__ import annotations


def test_health(client):
    response = client.get("/v1/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_magic_link_and_workspace_flow(client):
    request_response = client.post(
        "/v1/auth/magic-links/request",
        json={"email": "owner@example.com"},
    )
    assert request_response.status_code == 202
    preview_url = request_response.json()["preview_url"]
    token = preview_url.rsplit("=", 1)[1]

    verify_response = client.post("/v1/auth/magic-links/verify", json={"token": token})
    assert verify_response.status_code == 200
    session_token = verify_response.json()["session_token"]
    headers = {"Authorization": f"Bearer {session_token}"}

    create_workspace_response = client.post(
        "/v1/workspaces",
        headers=headers,
        json={"name": "Support Ops", "slug": "support-ops"},
    )
    assert create_workspace_response.status_code == 201
    workspace = create_workspace_response.json()
    workspace_id = workspace["workspace"]["id"]

    api_key_response = client.post(
        f"/v1/workspaces/{workspace_id}/api-keys",
        headers=headers,
        json={"label": "CLI"},
    )
    assert api_key_response.status_code == 201
    assert api_key_response.json()["secret"].startswith("rly_")

    audit_response = client.get(f"/v1/workspaces/{workspace_id}/audit", headers=headers)
    assert audit_response.status_code == 200
    assert len(audit_response.json()["items"]) >= 2
