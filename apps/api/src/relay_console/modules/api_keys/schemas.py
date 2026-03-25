from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApiKeyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    label: str
    key_prefix: str
    revoked_at: datetime | None = None
    created_at: datetime


class ApiKeyListResponse(BaseModel):
    items: list[ApiKeyOut]


class CreateApiKeyRequest(BaseModel):
    label: str
    scopes: list[str] = []
    expires_at: datetime | None = None


class CreateApiKeyResponse(BaseModel):
    api_key: ApiKeyOut
    secret: str
