from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from relay_console.api.deps import AuthContext, get_auth_context, get_db, get_request_id, require_workspace_role
from relay_console.modules.api_keys.schemas import ApiKeyListResponse, ApiKeyOut, CreateApiKeyRequest, CreateApiKeyResponse
from relay_console.modules.api_keys.service import create_api_key, list_api_keys, revoke_api_key


router = APIRouter()


@router.get("", response_model=ApiKeyListResponse)
def list_api_keys_endpoint(
    workspace_id: str,
    _: object = Depends(require_workspace_role("admin")),
    db: Session = Depends(get_db),
) -> ApiKeyListResponse:
    return list_api_keys(db=db, workspace_id=workspace_id)


@router.post("", response_model=CreateApiKeyResponse, status_code=201)
def create_api_key_endpoint(
    workspace_id: str,
    payload: CreateApiKeyRequest,
    context: AuthContext = Depends(get_auth_context),
    _: object = Depends(require_workspace_role("admin")),
    db: Session = Depends(get_db),
    request_id: str = Depends(get_request_id),
) -> CreateApiKeyResponse:
    return create_api_key(
        db=db,
        workspace_id=workspace_id,
        actor_user_id=context.user.id,
        label=payload.label,
        scopes=payload.scopes,
        expires_at=payload.expires_at,
        request_id=request_id,
    )


@router.post("/{api_key_id}/revoke", response_model=ApiKeyOut)
def revoke_api_key_endpoint(
    workspace_id: str,
    api_key_id: str,
    context: AuthContext = Depends(get_auth_context),
    _: object = Depends(require_workspace_role("admin")),
    db: Session = Depends(get_db),
    request_id: str = Depends(get_request_id),
) -> ApiKeyOut:
    return revoke_api_key(
        db=db,
        workspace_id=workspace_id,
        api_key_id=api_key_id,
        actor_user_id=context.user.id,
        request_id=request_id,
    )
