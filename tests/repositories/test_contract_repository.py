from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from cancion.common import (
    Action,
    ApprovalMode,
    Frequency,
)
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.repositories.contract import ContractRepository


def make_contract() -> Contract:
    now = datetime.now(UTC)

    return Contract(
        id=uuid4(),
        vendor="Netflix",
        action=Action.RENEW,
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
        created_at=now,
        updated_at=now,
    )


def test_save_and_get(session) -> None:
    repo = ContractRepository(session)

    contract = make_contract()

    repo.save(contract)

    loaded = repo.get(contract.id)

    print(contract.created_at, contract.created_at.tzinfo)
    print(loaded.created_at, loaded.created_at.tzinfo)

    assert loaded == contract


def test_list(session) -> None:
    repo = ContractRepository(session)

    contract = make_contract()

    repo.save(contract)

    contracts = repo.list()

    assert len(contracts) == 1
    assert contracts[0] == contract


def test_delete(session) -> None:
    repo = ContractRepository(session)

    contract = make_contract()

    repo.save(contract)

    assert repo.delete(contract.id)

    assert repo.get(contract.id) is None
