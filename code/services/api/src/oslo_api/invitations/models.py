from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class MembershipRole(StrEnum):
    OWNER = "owner"


class InvitationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass(frozen=True, slots=True)
class InviteMemberCommand:
    workspace_id: UUID
    invited_by_user_id: UUID
    email: str


@dataclass(frozen=True, slots=True)
class Invitation:
    id: UUID
    workspace_id: UUID
    invited_by_user_id: UUID
    email: str
    role: MembershipRole
    token_hash: bytes
    status: InvitationStatus
    created_at: datetime
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class IssuedInvitation:
    invitation: Invitation
    token: str = dataclass_field(repr=False)
