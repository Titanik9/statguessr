from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from relay_console.core.security import create_api_key_secret, hash_token, utcnow
from relay_console.modules.api_keys.models import ApiKey
from relay_console.modules.api_keys.schemas import ApiKeyListResponse, ApiKeyOut, CreateApiKeyResponse
from relay_console.modules.audit.service import record_audit_log


def list_api_keys(db: Session, workspace_id: str) -> ApiKeyListResponse:
    stmt = (
        select(ApiKey)
        .where(ApiKey.workspace_id == workspace_id)
        .order_by(ApiKey.created_at.desc())
    )
    items = [ApiKeyOut.model_validate(item) for item in db.execute(stmt).scalars().all()]
    return ApiKeyListResponse(items=items)


def create_api_key(
    db: Session,
    workspace_id: str,
    actor_user_id: str,
    label: str,
    scopes: list[str],
    expires_at,
    request_id: str,
) -> CreateApiKeyResponse:
    prefix, secret = create_api_key_secret()
    api_key = ApiKey(
        workspace_id=workspace_id,
        created_by_user_id=actor_user_id,
        label=label,
        key_prefix=prefix,
        key_hash=hash_token(secret),
        scopes_json=scopes or [],
        expires_at=expires_at,
        created_at=utcnow(),
    )
    db.add(api_key)
    db.flush()

    record_audit_log(
        db=db,
        workspace_id=workspace_id,
        actor_user_id=actor_user_id,
        action="api_key.create",
        target_type="api_key",
        target_id=api_key.id,
        after_json={"label": label, "key_prefix": prefix, "scopes": scopes},
        request_id=request_id,
    )
    db.commit()

    return CreateApiKeyResponse(api_key=ApiKeyOut.model_validate(api_key), secret=secret)


def revoke_api_key(
    db: Session,
    workspace_id: str,
    api_key_id: str,
    actor_user_id: str,
    request_id: str,
) -> ApiKeyOut:
    stmt = select(ApiKey).where(ApiKey.workspace_id == workspace_id, ApiKey.id == api_key_id)
    api_key = db.execute(stmt).scalar_one_or_none()
    if not api_key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")

    api_key.revoked_at = utcnow()
    record_audit_log(
        db=db,
        workspace_id=workspace_id,
        actor_user_id=actor_user_id,
        action="api_key.revoke",
        target_type="api_key",
        target_id=api_key.id,
        before_json={"revoked_at": None},
        after_json={"revoked_at": api_key.revoked_at.isoformat()},
        request_id=request_id,
    )
    db.commit()
    return ApiKeyOut.model_validate(api_key)
