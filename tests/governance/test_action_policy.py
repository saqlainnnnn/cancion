from decimal import Decimal

from cancion.common import Action, ApprovalMode, Frequency
from cancion.common.money import Money
from cancion.domain.contract import Contract
from cancion.governance.context import EvaluationContext, SpendRequest
from cancion.governance.policies.action import ActionRule
from cancion.governance.rule_result import RuleOutcome


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
    result = ActionRule().evaluate(make_context(Action.RENEW))

    assert result.outcome is RuleOutcome.PASS
    assert result.reason is None


def test_action_mismatch() -> None:
    result = ActionRule().evaluate(make_context(Action.CANCEL))

    assert result.outcome is RuleOutcome.FAIL
    assert result.reason == "Action mismatch: expected renew, got cancel."
