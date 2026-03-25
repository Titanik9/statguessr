from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from relay_console.db.base import Base, IdMixin, TimestampMixin


class Workspace(Base, IdMixin, TimestampMixin):
    __tablename__ = "workspaces"

    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    plan_tier: Mapped[str] = mapped_column(String(32), default="self-hosted")
    default_region: Mapped[str] = mapped_column(String(32), default="local")
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class WorkspaceMembership(Base, IdMixin, TimestampMixin):
    __tablename__ = "workspace_memberships"

    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str] = mapped_column(String(16), default="viewer", index=True)
    invited_by_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
