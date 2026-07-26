from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.db.mappers.contract import to_domain, to_model
from cancion.domain.contract import Contract, ContractStatus


def make_contract() -> Contract:
    now = datetime.now(UTC)

    return Contract(
        id=uuid4(),
        vendor="Netflix",
        action=Action.RENEW,
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
        status=ContractStatus.ACTIVE,
        version=1,
        agent_id=None,
        created_at=now,
        updated_at=now,
    )


def test_to_model() -> None:
    contract = make_contract()

    model = to_model(contract)

    assert model.id == contract.id
    assert model.vendor == contract.vendor
    assert model.action == contract.action
    assert model.max_amount == Decimal("18")
    assert model.frequency == contract.frequency
    assert model.approval_mode == contract.approval_mode
    assert model.status == contract.status
    assert model.version == contract.version
    assert model.agent_id == contract.agent_id
    assert model.created_at == contract.created_at
    assert model.updated_at == contract.updated_at


def test_to_domain() -> None:
    contract = make_contract()

    model = to_model(contract)

    restored = to_domain(model)

    assert restored == contract
