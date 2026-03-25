from __future__ import annotations

from fastapi import HTTPException, status
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session

from relay_console.core.security import utcnow
from relay_console.modules.audit.service import record_audit_log
from relay_console.modules.auth.models import User
from relay_console.modules.auth.schemas import UserOut
from relay_console.modules.auth.service import get_or_create_user
from relay_console.modules.iam.models import Workspace, WorkspaceMembership
from relay_console.modules.iam.schemas import WorkspaceListResponse, WorkspaceMemberOut, WorkspaceMembersResponse, WorkspaceOut


def serialize_membership(membership: WorkspaceMembership, user: User, workspace: Workspace) -> WorkspaceMemberOut:
    return WorkspaceMemberOut(
        id=membership.id,
        role=membership.role,
        user=UserOut.model_validate(user),
        workspace=WorkspaceOut.model_validate(workspace),
    )


def list_workspaces_for_user(db: Session, user_id: str) -> WorkspaceListResponse:
    stmt = (
        select(WorkspaceMembership, Workspace, User)
        .join(Workspace, Workspace.id == WorkspaceMembership.workspace_id)
        .join(User, User.id == WorkspaceMembership.user_id)
        .where(WorkspaceMembership.user_id == user_id)
        .order_by(Workspace.name.asc())
    )
    items = [serialize_membership(membership, user, workspace) for membership, workspace, user in db.execute(stmt).all()]
    return WorkspaceListResponse(items=items)


def create_workspace(db: Session, actor: User, name: str, slug: str, request_id: str) -> WorkspaceMemberOut:
    normalized_slug = slugify(slug or name)
    existing = db.execute(select(Workspace).where(Workspace.slug == normalized_slug)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Workspace slug is already in use.")

    workspace = Workspace(name=name, slug=normalized_slug, created_by_user_id=actor.id)
    db.add(workspace)
    db.flush()

    membership = WorkspaceMembership(
        workspace_id=workspace.id,
        user_id=actor.id,
        role="owner",
        invited_by_user_id=actor.id,
        joined_at=utcnow(),
        accepted_at=utcnow(),
    )
    db.add(membership)
    db.flush()

    record_audit_log(
        db=db,
        workspace_id=workspace.id,
        actor_user_id=actor.id,
        action="workspace.create",
        target_type="workspace",
        target_id=workspace.id,
        after_json={"name": workspace.name, "slug": workspace.slug},
        request_id=request_id,
    )
    db.commit()

    return serialize_membership(membership, actor, workspace)


def get_workspace_detail(db: Session, workspace_id: str, actor_id: str) -> WorkspaceMemberOut:
    stmt = (
        select(WorkspaceMembership, Workspace, User)
        .join(Workspace, Workspace.id == WorkspaceMembership.workspace_id)
        .join(User, User.id == WorkspaceMembership.user_id)
        .where(WorkspaceMembership.workspace_id == workspace_id, WorkspaceMembership.user_id == actor_id)
    )
    row = db.execute(stmt).one_or_none()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found.")
    membership, workspace, user = row
    return serialize_membership(membership, user, workspace)


def list_members(db: Session, workspace_id: str) -> WorkspaceMembersResponse:
    stmt = (
        select(WorkspaceMembership, Workspace, User)
        .join(Workspace, Workspace.id == WorkspaceMembership.workspace_id)
        .join(User, User.id == WorkspaceMembership.user_id)
        .where(WorkspaceMembership.workspace_id == workspace_id)
        .order_by(User.email.asc())
    )
    items = [serialize_membership(membership, user, workspace) for membership, workspace, user in db.execute(stmt).all()]
    return WorkspaceMembersResponse(items=items)


def upsert_member(
    db: Session,
    workspace_id: str,
    email: str,
    role: str,
    actor: User,
    request_id: str,
) -> WorkspaceMemberOut:
    if role not in {"owner", "admin", "editor", "viewer"}:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid role.")

    workspace = db.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found.")

    user = get_or_create_user(db, email=email)
    stmt = select(WorkspaceMembership).where(
        WorkspaceMembership.workspace_id == workspace_id,
        WorkspaceMembership.user_id == user.id,
    )
    membership = db.execute(stmt).scalar_one_or_none()
    before = None
    action = "workspace.member.create"

    if membership:
        before = {"role": membership.role}
        membership.role = role
        action = "workspace.member.update"
    else:
        membership = WorkspaceMembership(
            workspace_id=workspace_id,
            user_id=user.id,
            role=role,
            invited_by_user_id=actor.id,
            joined_at=None,
            accepted_at=None,
        )
        db.add(membership)
        db.flush()

    record_audit_log(
        db=db,
        workspace_id=workspace_id,
        actor_user_id=actor.id,
        action=action,
        target_type="workspace_membership",
        target_id=membership.id,
        before_json=before,
        after_json={"user_email": user.email, "role": membership.role},
        request_id=request_id,
    )
    db.commit()
    return serialize_membership(membership, user, workspace)
