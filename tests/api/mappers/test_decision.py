from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.api.mappers.decision import to_decision_response
from cancion.common import Action
from cancion.common.money import Money
from cancion.domain.decision import Decision, DecisionOutcome
from cancion.domain.decision_record import DecisionRecord


def test_to_decision_response_maps_domain_model():
    record = DecisionRecord(
        id=uuid4(),
        contract_id=uuid4(),
        vendor="Amazon",
        action=Action.PAY,
        amount=Money(Decimal("100")),
        decision=Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=[],
        ),
        created_at=datetime.now(UTC),
    )

    response = to_decision_response(record)

    assert response.id == record.id
    assert response.contract_id == record.contract_id

    assert response.vendor == record.vendor
    assert response.action == record.action

    assert response.amount.amount == Decimal("100")
    assert response.amount.currency == "USD"

    assert response.outcome == DecisionOutcome.APPROVE
    assert response.reasons == []

    assert response.created_at == record.created_at
