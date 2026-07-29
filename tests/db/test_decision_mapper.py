from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common import Action
from cancion.common.money import Money
from cancion.db.mappers.decision import (
    to_domain,
    to_model,
)
from cancion.domain.decision import (
    Decision,
    DecisionOutcome,
)
from cancion.domain.decision_record import DecisionRecord


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


def test_to_model() -> None:
    record = make_decision_record()

    model = to_model(record)

    assert model.id == record.id
    assert model.contract_id == record.contract_id
    assert model.vendor == record.vendor
    assert model.action == record.action
    assert model.amount == "20.00"
    assert model.currency == "USD"
    assert model.outcome == DecisionOutcome.APPROVE
    assert model.reasons == ["Approved"]
    assert model.created_at == record.created_at


def test_to_domain() -> None:
    record = make_decision_record()

    model = to_model(record)

    restored = to_domain(model)

    assert restored == record
