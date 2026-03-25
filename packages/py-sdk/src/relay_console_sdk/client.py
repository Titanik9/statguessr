from __future__ import annotations

from typing import Any

import httpx


class RelayClient:
    def __init__(self, base_url: str, session_token: str | None = None, api_key: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.session_token = session_token
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        headers = {"content-type": "application/json"}
        if self.session_token:
            headers["authorization"] = f"Bearer {self.session_token}"
        if self.api_key:
            headers["x-relay-key"] = self.api_key
        return headers

    def _request(self, method: str, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        response = httpx.request(method, f"{self.base_url}{path}", json=json, headers=self._headers(), timeout=30.0)
        response.raise_for_status()
        return response.json()

    def request_magic_link(self, email: str, workspace_slug: str | None = None) -> dict[str, Any]:
        return self._request("POST", "/auth/magic-links/request", {"email": email, "workspace_slug": workspace_slug})

    def verify_magic_link(self, token: str) -> dict[str, Any]:
        return self._request("POST", "/auth/magic-links/verify", {"token": token})

    def list_workspaces(self) -> dict[str, Any]:
        return self._request("GET", "/workspaces")

    def create_workspace(self, name: str, slug: str) -> dict[str, Any]:
        return self._request("POST", "/workspaces", {"name": name, "slug": slug})

    def create_api_key(self, workspace_id: str, label: str, scopes: list[str] | None = None) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/workspaces/{workspace_id}/api-keys",
            {"label": label, "scopes": scopes or []},
        )
