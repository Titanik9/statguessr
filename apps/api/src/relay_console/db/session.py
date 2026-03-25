from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from relay_console.core.config import get_settings
from relay_console.db.base import Base


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def initialize_database() -> None:
    from relay_console.modules.api_keys import models as api_keys_models  # noqa: F401
    from relay_console.modules.audit import models as audit_models  # noqa: F401
    from relay_console.modules.auth import models as auth_models  # noqa: F401
    from relay_console.modules.iam import models as iam_models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
