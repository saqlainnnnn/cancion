from decimal import Decimal

from cancion.common import ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.factory import ContractFactory
from cancion.domain.intent import Intent


def test_create_contract() -> None:
    intent = Intent(
        vendor="Netflix",
        action="renew",
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
    )

    contract = ContractFactory.create(intent)

    assert contract.vendor == intent.vendor
    assert contract.action == intent.action
    assert contract.max_amount == intent.max_amount
    assert contract.frequency == intent.frequency
    assert contract.approval_mode == intent.approval_mode
    assert contract.agent_id is None
