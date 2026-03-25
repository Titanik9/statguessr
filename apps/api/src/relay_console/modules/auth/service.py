from __future__ import annotations

from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from relay_console.core.config import get_settings
from relay_console.core.security import (
    build_magic_preview_url,
    create_session_token,
    ensure_utc,
    generate_magic_token,
    hash_token,
    utcnow,
)
from relay_console.modules.auth.models import AuthSession, MagicLinkToken, User
from relay_console.modules.auth.schemas import CurrentActorResponse, MagicLinkResponse, SessionResponse, UserOut
from relay_console.modules.iam.models import Workspace, WorkspaceMembership


def get_or_create_user(db: Session, email: str) -> User:
    stmt = select(User).where(User.email == email.lower())
    user = db.execute(stmt).scalar_one_or_none()
    if user:
        return user
    user = User(email=email.lower(), status="active")
    db.add(user)
    db.flush()
    return user


def request_magic_link(
    db: Session,
    email: str,
    workspace_slug: str | None,
    requested_ip: str | None,
) -> MagicLinkResponse:
    settings = get_settings()
    user = get_or_create_user(db, email=email)

    workspace = None
    if workspace_slug:
        stmt = select(Workspace).where(Workspace.slug == workspace_slug)
        workspace = db.execute(stmt).scalar_one_or_none()

    raw_token = generate_magic_token()
    expires_at = utcnow() + timedelta(minutes=settings.magic_link_ttl_minutes)
    magic_link = MagicLinkToken(
        user_id=user.id,
        workspace_id=workspace.id if workspace else None,
        token_hash=hash_token(raw_token),
        purpose="login",
        expires_at=expires_at,
        requested_ip=requested_ip,
        created_at=utcnow(),
    )
    db.add(magic_link)
    db.commit()

    preview_url = build_magic_preview_url(raw_token) if settings.auth_dev_preview else None
    return MagicLinkResponse(
        message="Magic link issued.",
        expires_at=expires_at,
        preview_url=preview_url,
    )


def verify_magic_link(
    db: Session,
    token: str,
    user_agent: str | None,
    ip_address: str | None,
) -> SessionResponse:
    stmt = select(MagicLinkToken).where(MagicLinkToken.token_hash == hash_token(token))
    magic_link = db.execute(stmt).scalar_one_or_none()
    now = utcnow()

    if not magic_link or magic_link.consumed_at is not None or ensure_utc(magic_link.expires_at) < now:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Magic link is invalid or expired.")

    user = db.get(User, magic_link.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    session = AuthSession(
        user_id=user.id,
        workspace_id=magic_link.workspace_id,
        session_hash=hash_token(generate_magic_token()),
        user_agent=user_agent,
        ip_address=ip_address,
        expires_at=now + timedelta(hours=get_settings().session_ttl_hours),
        last_seen_at=now,
        created_at=now,
    )
    db.add(session)
    db.flush()

    session_token = create_session_token(session.id, user.id)
    session.session_hash = hash_token(session_token)
    magic_link.consumed_at = now
    user.last_login_at = now
    db.commit()
    db.refresh(user)

    return SessionResponse(
        session_token=session_token,
        expires_at=session.expires_at,
        user=UserOut.model_validate(user),
    )


def current_actor(db: Session, user: User) -> CurrentActorResponse:
    stmt = (
        select(WorkspaceMembership, Workspace)
        .join(Workspace, Workspace.id == WorkspaceMembership.workspace_id)
        .where(WorkspaceMembership.user_id == user.id)
    )
    memberships = db.execute(stmt).all()
    items: list[dict] = []
    for membership, workspace in memberships:
        items.append(
            {
                "id": membership.id,
                "role": membership.role,
                "workspace": {
                    "id": workspace.id,
                    "name": workspace.name,
                    "slug": workspace.slug,
                    "plan_tier": workspace.plan_tier,
                },
            }
        )
    return CurrentActorResponse(user=UserOut.model_validate(user), workspaces=items)
