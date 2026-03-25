from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from relay_console.core.security import utcnow
from relay_console.modules.audit.models import AuditLog
from relay_console.modules.audit.schemas import AuditLogListResponse, AuditLogOut


def record_audit_log(
    db: Session,
    workspace_id: str | None,
    actor_user_id: str | None,
    action: str,
    target_type: str,
    target_id: str,
    request_id: str | None,
    before_json: dict | None = None,
    after_json: dict | None = None,
    actor_api_key_id: str | None = None,
) -> None:
    db.add(
        AuditLog(
            workspace_id=workspace_id,
            actor_user_id=actor_user_id,
            actor_api_key_id=actor_api_key_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            request_id=request_id,
            before_json=before_json,
            after_json=after_json,
            created_at=utcnow(),
        )
    )


def list_audit_logs(db: Session, workspace_id: str) -> AuditLogListResponse:
    stmt = (
        select(AuditLog)
        .where(AuditLog.workspace_id == workspace_id)
        .order_by(AuditLog.created_at.desc())
        .limit(100)
    )
    items = [AuditLogOut.model_validate(item) for item in db.execute(stmt).scalars().all()]
    return AuditLogListResponse(items=items)
