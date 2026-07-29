from calendar import monthrange
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from cancion.common import Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.domain.period import Period
from cancion.domain.spend_ledger import SpendLedger
from cancion.repositories.spend_ledger import SpendLedgerRepository


class SpendLedgerService:
    """Application service for cumulative spend tracking."""

    def __init__(
        self,
        repository: SpendLedgerRepository,
    ) -> None:
        self._repository = repository

    def current(
        self,
        contract: Contract,
        at: datetime | None = None,
    ) -> SpendLedger:
        """Return the active ledger for the contract, creating one if necessary."""

        at = self._normalize(at or datetime.now(UTC))

        ledger = self._repository.get_active(
            contract.id,
            at,
        )

        if ledger is not None:
            return ledger

        period = self.current_period(
            contract.frequency,
            at,
        )

        ledger = SpendLedger(
            contract_id=contract.id,
            period_start=period.start,
            period_end=period.end,
            spent_amount=Money(
                Decimal("0"),
                contract.max_amount.currency,
            ),
        )

        self._repository.save(ledger)

        return ledger

    def record_spend(
        self,
        contract: Contract,
        amount: Money,
        at: datetime | None = None,
    ) -> SpendLedger:
        """Record successful spend for a contract."""

        ledger = self.current(
            contract,
            at,
        )

        updated = ledger.add(amount)

        self._repository.save(updated)

        return updated

    def current_period(
        self,
        frequency: Frequency,
        at: datetime,
    ) -> Period:
        """Return the billing period containing the supplied timestamp."""

        at = self._normalize(at)

        if frequency is Frequency.DAILY:
            start = at.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            end = start + timedelta(days=1)

        elif frequency is Frequency.WEEKLY:
            start = (at - timedelta(days=at.weekday())).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            end = start + timedelta(days=7)

        elif frequency is Frequency.MONTHLY:
            start = at.replace(
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            end = start.replace(
                day=monthrange(
                    start.year,
                    start.month,
                )[1],
            ) + timedelta(days=1)

        elif frequency is Frequency.YEARLY:
            start = at.replace(
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            end = start.replace(year=start.year + 1)

        else:
            raise ValueError(f"Unsupported frequency: {frequency}")

        return Period(
            start=start,
            end=end,
        )

    @staticmethod
    def _normalize(
        dt: datetime,
    ) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)

        return dt.astimezone(UTC)
