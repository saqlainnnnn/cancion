from decimal import Decimal

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.governance.context import EvaluationContext, SpendRequest
from cancion.governance.policies.action import ActionRule


def make_context(action: Action) -> EvaluationContext:
    contract = Contract(
        vendor="Netflix",
        action=Action.RENEW,
        max_amount=Money(Decimal("18")),
        frequency=Frequency.MONTHLY,
        approval_mode=ApprovalMode.AUTO,
    )

    request = SpendRequest(
        vendor="Netflix",
        action=action,
        amount=Money(Decimal("18")),
    )

    return EvaluationContext(
        contract=contract,
        request=request,
    )


def test_action_matches() -> None:
    assert ActionRule().evaluate(make_context(Action.RENEW)) is None


def test_action_mismatch() -> None:
    result = ActionRule().evaluate(make_context(Action.CANCEL))

    assert result is not None
    assert "Action mismatch" in result
