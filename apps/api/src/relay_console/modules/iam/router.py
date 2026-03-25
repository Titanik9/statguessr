from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from relay_console.api.deps import AuthContext, get_auth_context, get_db, get_request_id, require_workspace_role
from relay_console.modules.iam.schemas import CreateWorkspaceRequest, UpsertWorkspaceMemberRequest, WorkspaceListResponse, WorkspaceMemberOut, WorkspaceMembersResponse
from relay_console.modules.iam.service import create_workspace, get_workspace_detail, list_members, list_workspaces_for_user, upsert_member


router = APIRouter()


@router.get("", response_model=WorkspaceListResponse)
def list_workspaces_endpoint(
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
) -> WorkspaceListResponse:
    return list_workspaces_for_user(db=db, user_id=context.user.id)


@router.post("", response_model=WorkspaceMemberOut, status_code=201)
def create_workspace_endpoint(
    payload: CreateWorkspaceRequest,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
    request_id: str = Depends(get_request_id),
) -> WorkspaceMemberOut:
    return create_workspace(db=db, actor=context.user, name=payload.name, slug=payload.slug, request_id=request_id)


@router.get("/{workspace_id}", response_model=WorkspaceMemberOut)
def get_workspace_endpoint(
    workspace_id: str,
    context: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db),
) -> WorkspaceMemberOut:
    return get_workspace_detail(db=db, workspace_id=workspace_id, actor_id=context.user.id)


@router.get("/{workspace_id}/members", response_model=WorkspaceMembersResponse)
def list_members_endpoint(
    workspace_id: str,
    _: object = Depends(require_workspace_role("viewer")),
    db: Session = Depends(get_db),
) -> WorkspaceMembersResponse:
    return list_members(db=db, workspace_id=workspace_id)


@router.post("/{workspace_id}/members", response_model=WorkspaceMemberOut)
def upsert_member_endpoint(
    workspace_id: str,
    payload: UpsertWorkspaceMemberRequest,
    context: AuthContext = Depends(get_auth_context),
    _: object = Depends(require_workspace_role("admin")),
    db: Session = Depends(get_db),
    request_id: str = Depends(get_request_id),
) -> WorkspaceMemberOut:
    return upsert_member(
        db=db,
        workspace_id=workspace_id,
        email=payload.email,
        role=payload.role,
        actor=context.user,
        request_id=request_id,
    )
