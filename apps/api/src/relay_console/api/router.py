from __future__ import annotations

from fastapi import APIRouter

from relay_console.modules.api_keys.router import router as api_keys_router
from relay_console.modules.audit.router import router as audit_router
from relay_console.modules.auth.router import router as auth_router
from relay_console.modules.health.router import router as health_router
from relay_console.modules.iam.router import router as iam_router


api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(iam_router, prefix="/workspaces", tags=["Workspaces"])
api_router.include_router(api_keys_router, prefix="/workspaces/{workspace_id}/api-keys", tags=["API Keys"])
api_router.include_router(audit_router, prefix="/workspaces/{workspace_id}/audit", tags=["Audit"])
