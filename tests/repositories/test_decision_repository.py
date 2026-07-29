from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common import Action
from cancion.common.money import Money
from cancion.domain.decision import (
    Decision,
    DecisionOutcome,
)
from cancion.domain.decision_record import DecisionRecord
from cancion.repositories.decision import DecisionRepository


def make_decision_record() -> DecisionRecord:
    now = datetime.now(UTC)

    return DecisionRecord(
        id=uuid4(),
        contract_id=uuid4(),
        vendor="Netflix",
        action=Action.PAY,
        amount=Money(
            amount=Decimal("20.00"),
            currency="USD",
        ),
        decision=Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=["Approved"],
        ),
        created_at=now,
    )


def test_save_and_get(session) -> None:
    repo = DecisionRepository(session)

    record = make_decision_record()

    repo.save(record)

    loaded = repo.get(record.id)

    assert loaded == record


def test_list_all(session) -> None:
    repo = DecisionRepository(session)

    record = make_decision_record()

    repo.save(record)

    records = repo.list_all()

    assert len(records) == 1
    assert records[0] == record


def test_list_by_contract(session) -> None:
    repo = DecisionRepository(session)

    contract_id = uuid4()

    now = datetime.now(UTC)

    record1 = DecisionRecord(
        id=uuid4(),
        contract_id=contract_id,
        vendor="Netflix",
        action=Action.PAY,
        amount=Money(
            amount=Decimal("20.00"),
            currency="USD",
        ),
        decision=Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=["Approved"],
        ),
        created_at=now,
    )

    record2 = DecisionRecord(
        id=uuid4(),
        contract_id=uuid4(),
        vendor="Spotify",
        action=Action.PAY,
        amount=Money(
            amount=Decimal("15.00"),
            currency="USD",
        ),
        decision=Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=["Approved"],
        ),
        created_at=now,
    )

    repo.save(record1)
    repo.save(record2)

    records = repo.list_by_contract(contract_id)

    assert records == [record1]


def test_delete(session) -> None:
    repo = DecisionRepository(session)

    record = make_decision_record()

    repo.save(record)

    assert repo.delete(record.id)

    assert repo.get(record.id) is None
