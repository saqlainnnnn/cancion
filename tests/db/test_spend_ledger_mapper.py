from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common.money import Money
from cancion.db.mappers.spend_ledger import to_domain, to_model
from cancion.domain.spend_ledger import SpendLedger


def test_to_model():
    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("45.50")),
    )

    model = to_model(ledger)

    assert model.id == ledger.id
    assert model.contract_id == ledger.contract_id
    assert model.period_start == ledger.period_start
    assert model.period_end == ledger.period_end
    assert model.spent_amount == Decimal("45.50")
    assert model.currency == "USD"


def test_to_domain():
    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("87.25")),
    )

    restored = to_domain(to_model(ledger))

    assert restored == ledger
