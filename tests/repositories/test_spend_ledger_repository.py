from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common.money import Money
from cancion.db.models.spend_ledger import SpendLedgerModel
from cancion.domain.spend_ledger import SpendLedger
from cancion.repositories.spend_ledger import SpendLedgerRepository


def test_save(session):
    repo = SpendLedgerRepository(session)

    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("20")),
    )

    repo.save(ledger)

    model = session.get(
        SpendLedgerModel,
        ledger.id,
    )

    assert model is not None
    assert model.spent_amount == Decimal("20")


def test_get(session):
    repo = SpendLedgerRepository(session)

    ledger = SpendLedger(
        contract_id=uuid4(),
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("99")),
    )

    repo.save(ledger)

    restored = repo.get(ledger.id)

    assert restored == ledger


def test_get_returns_none(session):
    repo = SpendLedgerRepository(session)

    assert repo.get(uuid4()) is None


def test_get_active(session):
    repo = SpendLedgerRepository(session)

    contract_id = uuid4()

    ledger = SpendLedger(
        contract_id=contract_id,
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("50")),
    )

    repo.save(ledger)

    active = repo.get_active(
        contract_id,
        datetime(2026, 7, 15, tzinfo=UTC),
    )

    assert active == ledger


def test_get_active_returns_none(session):
    repo = SpendLedgerRepository(session)

    assert (
        repo.get_active(
            uuid4(),
            datetime.now(UTC),
        )
        is None
    )


def test_list_for_contract(session):
    repo = SpendLedgerRepository(session)

    contract_id = uuid4()

    july = SpendLedger(
        contract_id=contract_id,
        period_start=datetime(2026, 7, 1, tzinfo=UTC),
        period_end=datetime(2026, 8, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("20")),
    )

    august = SpendLedger(
        contract_id=contract_id,
        period_start=datetime(2026, 8, 1, tzinfo=UTC),
        period_end=datetime(2026, 9, 1, tzinfo=UTC),
        spent_amount=Money(Decimal("80")),
    )

    repo.save(july)
    repo.save(august)

    ledgers = repo.list_for_contract(contract_id)

    assert len(ledgers) == 2
    assert ledgers[0].period_start > ledgers[1].period_start
