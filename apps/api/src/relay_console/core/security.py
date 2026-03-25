from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from relay_console.core.config import get_settings


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def generate_id() -> str:
    return str(uuid4())


def hash_token(value: str) -> str:
    secret = get_settings().jwt_secret
    return hashlib.sha256(f"{secret}:{value}".encode("utf-8")).hexdigest()


def generate_magic_token() -> str:
    return secrets.token_urlsafe(32)


def build_magic_preview_url(token: str) -> str:
    base = get_settings().public_base_url.rstrip("/")
    return f"{base}/auth/sign-in?token={token}"


def create_session_token(session_id: str, user_id: str) -> str:
    settings = get_settings()
    expires_at = utcnow() + timedelta(hours=settings.session_ttl_hours)
    payload = {"session_id": session_id, "sub": user_id, "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_session_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])


def create_api_key_secret() -> tuple[str, str]:
    raw = f"rly_{secrets.token_urlsafe(24)}"
    return raw[:12], raw
