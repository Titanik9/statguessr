from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    display_name: str | None = None


class MagicLinkRequest(BaseModel):
    email: EmailStr
    workspace_slug: str | None = None


class MagicLinkResponse(BaseModel):
    message: str
    expires_at: datetime
    preview_url: str | None = None


class MagicLinkVerifyRequest(BaseModel):
    token: str


class SessionResponse(BaseModel):
    session_token: str
    expires_at: datetime
    user: UserOut


class CurrentActorResponse(BaseModel):
    user: UserOut
    workspaces: list[dict]
