from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common import Action
from cancion.common.money import Money
from cancion.domain.decision import Decision, DecisionOutcome
from cancion.domain.decision_record import DecisionRecord
from cancion.repositories.decision import DecisionRepository
from cancion.services.decision import DecisionService


def make_record(
    vendor: str = "Netflix",
) -> DecisionRecord:
    return DecisionRecord(
        id=uuid4(),
        contract_id=uuid4(),
        vendor=vendor,
        action=Action.RENEW,
        amount=Money(Decimal("15")),
        decision=Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=[],
        ),
        created_at=datetime.now(UTC),
    )


def make_service(session):
    repository = DecisionRepository(session)
    return DecisionService(repository)


def test_get(session):
    service = make_service(session)

    record = make_record()

    service._repository.save(record)

    assert service.get(record.id) == record


def test_list(session):
    service = make_service(session)

    first = make_record("Netflix")
    second = make_record("Spotify")

    service._repository.save(first)
    service._repository.save(second)

    decisions = service.list()

    assert len(decisions) == 2


def test_list_by_contract(session):
    service = make_service(session)

    contract_id = uuid4()

    first = DecisionRecord(
        id=uuid4(),
        contract_id=contract_id,
        vendor="Netflix",
        action=Action.RENEW,
        amount=Money(Decimal("10")),
        decision=Decision(
            outcome=DecisionOutcome.APPROVE,
            reasons=[],
        ),
        created_at=datetime.now(UTC),
    )

    second = make_record()

    service._repository.save(first)
    service._repository.save(second)

    decisions = service.list_by_contract(contract_id)

    assert len(decisions) == 1
    assert decisions[0].contract_id == contract_id


def test_delete(session):
    service = make_service(session)

    record = make_record()

    service._repository.save(record)

    assert service.delete(record.id)

    assert service.get(record.id) is None
