from datetime import UTC, datetime
from decimal import Decimal

from cancion.common.money import Money
from cancion.db.models.spend_ledger import SpendLedgerModel
from cancion.domain.spend_ledger import SpendLedger


def to_model(ledger: SpendLedger) -> SpendLedgerModel:
    return SpendLedgerModel(
        id=ledger.id,
        contract_id=ledger.contract_id,
        period_start=ledger.period_start,
        period_end=ledger.period_end,
        spent_amount=ledger.spent_amount.amount,
        currency=ledger.spent_amount.currency,
        created_at=ledger.created_at,
        updated_at=ledger.updated_at,
    )


def to_domain(model: SpendLedgerModel) -> SpendLedger:
    return SpendLedger(
        id=model.id,
        contract_id=model.contract_id,
        period_start=_normalize_datetime(model.period_start),
        period_end=_normalize_datetime(model.period_end),
        spent_amount=Money(
            amount=Decimal(model.spent_amount),
            currency=model.currency,
        ),
        created_at=_normalize_datetime(model.created_at),
        updated_at=_normalize_datetime(model.updated_at),
    )


def _normalize_datetime(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)

    return dt.astimezone(UTC)
