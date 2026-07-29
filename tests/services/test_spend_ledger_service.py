from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract, ContractStatus
from cancion.repositories.spend_ledger import SpendLedgerRepository
from cancion.services.spend_ledger import SpendLedgerService


def make_contract() -> Contract:
    return Contract(
        id=uuid4(),
        vendor="OpenAI",
        action=Action.PAY,
        max_amount=Money(
            Decimal("1000"),
            "USD",
        ),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
        status=ContractStatus.ACTIVE,
        version=1,
        agent_id="agent-1",
    )


def test_get_or_create_creates_new_ledger(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    contract = make_contract()

    ledger = service.current(contract)

    assert ledger.contract_id == contract.id
    assert ledger.spent_amount == Money(
        Decimal("0"),
        "USD",
    )


def test_get_or_create_returns_existing_ledger(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    contract = make_contract()

    first = service.current(contract)
    second = service.current(contract)

    assert first.id == second.id


def test_record_spend_updates_amount(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    contract = make_contract()

    ledger = service.record_spend(
        contract,
        Money(
            Decimal("125"),
            "USD",
        ),
    )

    assert ledger.spent_amount == Money(
        Decimal("125"),
        "USD",
    )


def test_record_spend_accumulates(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    contract = make_contract()

    service.record_spend(
        contract,
        Money(
            Decimal("100"),
            "USD",
        ),
    )

    ledger = service.record_spend(
        contract,
        Money(
            Decimal("250"),
            "USD",
        ),
    )

    assert ledger.spent_amount == Money(
        Decimal("350"),
        "USD",
    )


def test_current_period_monthly(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    period = service.current_period(
        Frequency.MONTHLY,
        datetime(
            2026,
            7,
            17,
            tzinfo=UTC,
        ),
    )

    assert period.start == datetime(
        2026,
        7,
        1,
        tzinfo=UTC,
    )

    assert period.end == datetime(
        2026,
        8,
        1,
        tzinfo=UTC,
    )


def test_current_period_weekly(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    period = service.current_period(
        Frequency.WEEKLY,
        datetime(
            2026,
            7,
            15,
            tzinfo=UTC,
        ),
    )

    assert period.contains(
        datetime(
            2026,
            7,
            17,
            tzinfo=UTC,
        ),
    )


def test_current_period_daily(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    period = service.current_period(
        Frequency.DAILY,
        datetime(
            2026,
            7,
            15,
            12,
            30,
            tzinfo=UTC,
        ),
    )

    assert period.start == datetime(
        2026,
        7,
        15,
        tzinfo=UTC,
    )

    assert period.end == datetime(
        2026,
        7,
        16,
        tzinfo=UTC,
    )


def test_current_period_yearly(
    session,
):
    repository = SpendLedgerRepository(session)
    service = SpendLedgerService(repository)

    period = service.current_period(
        Frequency.YEARLY,
        datetime(
            2026,
            10,
            5,
            tzinfo=UTC,
        ),
    )

    assert period.start == datetime(
        2026,
        1,
        1,
        tzinfo=UTC,
    )

    assert period.end == datetime(
        2027,
        1,
        1,
        tzinfo=UTC,
    )
