from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money


class ContractStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    REVOKED = "revoked"


@dataclass(frozen=True, slots=True)
class Contract:
    """Represents an approved spending contract."""

    vendor: str
    action: Action
    max_amount: Money
    frequency: Frequency

    agent_id: UUID | None = None
    approval_mode: ApprovalMode = ApprovalMode.AUTO

    status: ContractStatus = ContractStatus.ACTIVE
    version: int = 1

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
