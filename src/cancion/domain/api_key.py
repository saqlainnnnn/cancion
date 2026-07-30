from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


def _utc_now() -> datetime:
    return datetime.now(UTC)


class ApiKeyStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"


@dataclass(frozen=True, slots=True)
class ApiKey:
    agent_id: UUID
    name: str
    key_hash: str
    status: ApiKeyStatus = ApiKeyStatus.ACTIVE

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)
