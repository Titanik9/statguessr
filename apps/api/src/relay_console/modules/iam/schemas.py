from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr

from relay_console.modules.auth.schemas import UserOut


class WorkspaceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    plan_tier: str


class WorkspaceMemberOut(BaseModel):
    id: str
    role: str
    user: UserOut
    workspace: WorkspaceOut


class WorkspaceListResponse(BaseModel):
    items: list[WorkspaceMemberOut]


class CreateWorkspaceRequest(BaseModel):
    name: str
    slug: str


class UpsertWorkspaceMemberRequest(BaseModel):
    email: EmailStr
    role: str


class WorkspaceMembersResponse(BaseModel):
    items: list[WorkspaceMemberOut]
