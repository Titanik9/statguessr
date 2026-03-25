from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/health")


@router.get("/live")
def live() -> dict[str, str]:
    return {"status": "ok", "service": "relay-console-api"}


@router.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ok", "service": "relay-console-api"}
