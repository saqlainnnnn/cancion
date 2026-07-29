from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from uuid import UUID, uuid4

from cancion.common.money import Money


@dataclass(frozen=True, slots=True)
class SpendLedger:
    """Tracks cumulative spending for a contract within a billing period."""

    contract_id: UUID

    period_start: datetime
    period_end: datetime

    spent_amount: Money

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def add(self, amount: Money) -> "SpendLedger":
        """Return a new ledger with the additional spend applied."""

        if amount.currency != self.spent_amount.currency:
            raise ValueError("Currency mismatch between ledger and requested amount.")

        return replace(
            self,
            spent_amount=Money(
                amount=self.spent_amount.amount + amount.amount,
                currency=self.spent_amount.currency,
            ),
            updated_at=datetime.now(UTC),
        )

    def contains(self, instant: datetime) -> bool:
        """Return whether the given instant falls within this ledger period."""
        instant = instant.replace(tzinfo=UTC) if instant.tzinfo is None else instant.astimezone(UTC)

        return self.period_start <= instant < self.period_end
