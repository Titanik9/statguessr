from __future__ import annotations

from celery import Celery

from relay_console.core.config import get_settings


settings = get_settings()
celery_app = Celery("relay_console", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_default_queue = "relay-console"


@celery_app.task(name="relay_console.healthcheck")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": "relay-console-worker"}
