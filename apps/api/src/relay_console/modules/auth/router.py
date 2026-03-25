from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from relay_console.api.deps import get_auth_context, get_db
from relay_console.modules.auth.schemas import (
    CurrentActorResponse,
    MagicLinkRequest,
    MagicLinkResponse,
    MagicLinkVerifyRequest,
    SessionResponse,
)
from relay_console.modules.auth.service import current_actor, request_magic_link, verify_magic_link


router = APIRouter()


@router.post("/magic-links/request", response_model=MagicLinkResponse, status_code=202)
def request_magic_link_endpoint(payload: MagicLinkRequest, request: Request, db: Session = Depends(get_db)) -> MagicLinkResponse:
    return request_magic_link(
        db=db,
        email=payload.email,
        workspace_slug=payload.workspace_slug,
        requested_ip=request.client.host if request.client else None,
    )


@router.post("/magic-links/verify", response_model=SessionResponse)
def verify_magic_link_endpoint(payload: MagicLinkVerifyRequest, request: Request, db: Session = Depends(get_db)) -> SessionResponse:
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    return verify_magic_link(db=db, token=payload.token, user_agent=user_agent, ip_address=ip_address)


@router.get("/me", response_model=CurrentActorResponse)
def current_actor_endpoint(context=Depends(get_auth_context), db: Session = Depends(get_db)) -> CurrentActorResponse:
    return current_actor(db=db, user=context.user)
