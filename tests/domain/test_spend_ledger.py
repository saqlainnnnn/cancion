from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common.money import Money
from cancion.domain.spend_ledger import SpendLedger


def test_add_returns_new_ledger():
    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("20.00")),
    )

    updated = ledger.add(Money(Decimal("30.00")))

    assert updated.spent_amount.amount == Decimal("50.00")
    assert ledger.spent_amount.amount == Decimal("20.00")


def test_contains_inside_period():
    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("0")),
    )

    assert ledger.contains(datetime(2026, 7, 15, tzinfo=UTC))


def test_contains_outside_period():
    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("0")),
    )

    assert not ledger.contains(datetime(2026, 8, 5, tzinfo=UTC))


def test_add_rejects_currency_mismatch():
    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(
            Decimal("10"),
            "USD",
        ),
    )

    try:
        ledger.add(
            Money(
                Decimal("5"),
                "EUR",
            )
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError.")
