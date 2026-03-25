from __future__ import annotations

from sqlalchemy import select

from relay_console.core.security import utcnow
from relay_console.db.session import SessionLocal, initialize_database
from relay_console.modules.auth.models import User
from relay_console.modules.iam.models import Workspace, WorkspaceMembership


def seed_phase_two_demo() -> None:
    initialize_database()
    with SessionLocal() as db:
        existing = db.execute(select(User).where(User.email == "demo@relay-console.local")).scalar_one_or_none()
        if existing:
            return

        user = User(email="demo@relay-console.local", display_name="Demo Owner", status="active")
        db.add(user)
        db.flush()

        workspace = Workspace(
            name="Demo Workspace",
            slug="demo-workspace",
            created_by_user_id=user.id,
            plan_tier="self-hosted",
            default_region="local",
        )
        db.add(workspace)
        db.flush()

        membership = WorkspaceMembership(
            workspace_id=workspace.id,
            user_id=user.id,
            role="owner",
            invited_by_user_id=user.id,
            joined_at=utcnow(),
            accepted_at=utcnow(),
        )
        db.add(membership)
        db.commit()


if __name__ == "__main__":
    seed_phase_two_demo()
