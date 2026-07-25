from decimal import Decimal
from uuid import uuid4

import pytest

from cancion.domain.contract import Contract, ContractStatus
from cancion.domain.intent import ApprovalMode, Frequency


def test_contract_creation():
    contract = Contract(
        agent_id=uuid4(),
        vendor="Netflix",
        action="renew",
        max_amount=Decimal("18.00"),
        frequency=Frequency.MONTHLY,
    )

    assert contract.vendor == "Netflix"
    assert contract.status == ContractStatus.ACTIVE
    assert contract.version == 1
    assert contract.approval_mode == ApprovalMode.AUTO


def test_contract_is_immutable():
    contract = Contract(
        agent_id=uuid4(),
        vendor="Netflix",
        action="renew",
        max_amount=Decimal("18.00"),
        frequency=Frequency.MONTHLY,
    )

    with pytest.raises(AttributeError):
        contract.vendor = "Spotify"  # type: ignore[misc]
