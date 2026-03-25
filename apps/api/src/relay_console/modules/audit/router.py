from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from relay_console.api.deps import get_db, require_workspace_role
from relay_console.modules.audit.schemas import AuditLogListResponse
from relay_console.modules.audit.service import list_audit_logs


router = APIRouter()


@router.get("", response_model=AuditLogListResponse)
def list_audit_logs_endpoint(
    workspace_id: str,
    _: object = Depends(require_workspace_role("admin")),
    db: Session = Depends(get_db),
) -> AuditLogListResponse:
    return list_audit_logs(db=db, workspace_id=workspace_id)
