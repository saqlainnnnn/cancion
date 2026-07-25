from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from cancion.common import ApprovalMode, Frequency
from cancion.common.money import Money


class ContractStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    REVOKED = "revoked"


@dataclass(frozen=True, slots=True)
class Contract:
    """Represents an approved spending contract."""

    agent_id: UUID
    vendor: str
    action: str
    max_amount: Money
    frequency: Frequency

    approval_mode: ApprovalMode = ApprovalMode.AUTO

    status: ContractStatus = ContractStatus.ACTIVE
    version: int = 1

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
