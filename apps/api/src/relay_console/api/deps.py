from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from relay_console.core.security import decode_session_token, ensure_utc, hash_token, utcnow
from relay_console.db.session import get_db_session
from relay_console.modules.api_keys.models import ApiKey
from relay_console.modules.auth.models import AuthSession, User
from relay_console.modules.iam.models import WorkspaceMembership


ROLE_ORDER = {"viewer": 10, "editor": 20, "admin": 30, "owner": 40}


@dataclass
class AuthContext:
    user: User
    session: AuthSession


def get_db() -> Session:
    yield from get_db_session()


def get_auth_context(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> AuthContext:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")

    raw_token = authorization.split(" ", 1)[1].strip()
    payload = decode_session_token(raw_token)
    session_hash = hash_token(raw_token)

    session = db.get(AuthSession, payload["session_id"])
    if not session or session.session_hash != session_hash or session.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session.")
    if ensure_utc(session.expires_at) < utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired.")

    user = db.get(User, session.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

    return AuthContext(user=user, session=session)


def get_current_user(context: AuthContext = Depends(get_auth_context)) -> User:
    return context.user


def get_workspace_membership(
    workspace_id: str,
    context: AuthContext,
    db: Session,
) -> WorkspaceMembership:
    stmt = select(WorkspaceMembership).where(
        WorkspaceMembership.workspace_id == workspace_id,
        WorkspaceMembership.user_id == context.user.id,
    )
    membership = db.execute(stmt).scalar_one_or_none()
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace membership not found.")
    return membership


def require_workspace_role(
    minimum_role: str,
):
    def dependency(
        workspace_id: str,
        context: AuthContext = Depends(get_auth_context),
        db: Session = Depends(get_db),
    ) -> WorkspaceMembership:
        membership = get_workspace_membership(workspace_id=workspace_id, context=context, db=db)
        if ROLE_ORDER[membership.role] < ROLE_ORDER[minimum_role]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient workspace role.")
        return membership

    return dependency


def get_request_id(request: Request) -> str:
    return request.state.request_id


def get_api_key(
    x_relay_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> ApiKey | None:
    if not x_relay_key:
        return None
    hashed = hash_token(x_relay_key)
    stmt = select(ApiKey).where(ApiKey.key_hash == hashed, ApiKey.revoked_at.is_(None))
    return db.execute(stmt).scalar_one_or_none()
