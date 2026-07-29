from dataclasses import dataclass, field, replace
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

    def update(
        self,
        *,
        vendor: str | None = None,
        action: Action | None = None,
        max_amount: Money | None = None,
        frequency: Frequency | None = None,
        approval_mode: ApprovalMode | None = None,
    ) -> "Contract":
        """Return an updated copy of this contract."""

        return replace(
            self,
            vendor=vendor if vendor is not None else self.vendor,
            action=action if action is not None else self.action,
            max_amount=max_amount if max_amount is not None else self.max_amount,
            frequency=frequency if frequency is not None else self.frequency,
            approval_mode=(approval_mode if approval_mode is not None else self.approval_mode),
            version=self.version + 1,
            updated_at=datetime.now(UTC),
        )
